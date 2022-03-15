import frappe
from frappe.utils import getdate, get_time, cint, now

from amh_rentals_erpnext.stock import get_sl_entry
from ..rental_voucher_event import RentalVoucherEvent


def up(event: RentalVoucherEvent):
    rental_voucher = frappe.get_doc("Rental Voucher", event.rental_voucher)

    # Validate returnability
    for item in event.items:
        voucher_item = [x for x in rental_voucher.items if x.item == item.item][0]
        if item.qty > (voucher_item.qty - voucher_item.qty_returned):
            frappe.throw("You cannot return more than that was taken")

    # Make SLEs
    make_stock_entries(event, rental_voucher)

    # Update RentalVoucher
    for item in event.items:
        voucher_item = [x for x in rental_voucher.items if x.item == item.item][0]
        voucher_item.qty_returned = cint((voucher_item.qty_returned or 0) + item.qty)

    rental_voucher.flags.ignore_validate_update_after_submit = True
    rental_voucher.save(ignore_permissions=True)


def down(event: RentalVoucherEvent):
    rental_voucher = frappe.get_doc("Rental Voucher", event.rental_voucher)

    # Cancel SLEs
    make_stock_entries(event, rental_voucher)

    # Update RentalVoucher
    for item in event.items:
        voucher_item = [x for x in rental_voucher.items if x.item == item.item][0]
        voucher_item.qty_returned = cint((item.qty_returned or 0) - item.qty)

    rental_voucher.flags.ignore_validate_update_after_submit = True
    rental_voucher.save(ignore_permissions=True)


def make_stock_entries(event: RentalVoucherEvent, rental_voucher):

    from_wh = frappe.get_single("Stock Settings").rented_warehouse
    if not from_wh:
        frappe.throw("Please define Rented Warehouse in Stock Settings")

    target_wh = frappe.db.get_value("Branch", rental_voucher.branch, "warehouse")
    if not target_wh:
        frappe.throw("Please define Warehouse on Branch")

    sl_entries = []
    for item in event.items:
        item_doc = frappe.get_doc("Item", item.item)
        if not item_doc.is_stock_item:
            frappe.throw("Cannot return non-stock item: " + item.name)

        _commons = dict(
            item_code=item.item,
            posting_date=getdate(now()),
            posting_time=get_time(now()),
            doctype=event.doctype,
            name=event.name,
            child_name=item.name,
            docstatus=event.docstatus,
        )

        # FROM WH
        sl_entries.append(get_sl_entry(dict(
            **_commons,
            warehouse=from_wh,
            stock_qty=-1 * item.qty,
        )))

        # TO WH
        sl_entries.append(get_sl_entry(dict(
            **_commons,
            warehouse=target_wh,
            stock_qty=item.qty,
        )))

    # reverse sl entries if cancel
    if event.docstatus == 2:
        sl_entries.reverse()

    from erpnext.stock.stock_ledger import make_sl_entries
    make_sl_entries(sl_entries)
