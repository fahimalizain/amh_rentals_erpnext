# Copyright (c) 2022, Fahim Ali Zain and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt, cint, add_days, getdate, get_time, now

from amh_rentals_erpnext import RENTAL_ITEM_GROUPS, RentalVoucherEventType
from amh_rentals_erpnext.stock import get_sl_entry


class RentalVoucher(Document):
    def validate(self):
        self.validate_items()
        self.calculate()
        if not self.date_time:
            self.date_time = now()

    def before_update_after_submit(self):
        self.calculate()

    def on_submit(self):
        self.make_stock_ledger_entries()

    def on_cancel(self):
        self.make_stock_ledger_entries()
        self.ignore_linked_doctypes = ('GL Entry', 'Stock Ledger Entry', 'Repost Item Valuation')

    def validate_items(self):
        item_map = dict()
        for i in range(len(self.items) - 1, -1, -1):
            item = self.items[i]
            if item.item in item_map:
                item_map[item.item].qty += item.qty
                self.items.remove(item)

            item_details = frappe.db.get_value(
                "Item", item.item, ["name", "item_group", "daily_rate", "max_rent_days"], as_dict=1)

            if item_details.item_group not in RENTAL_ITEM_GROUPS:
                frappe.throw("Non-Rentable Item")

            item.max_rent_days = item_details.max_rent_days
            item.daily_rate = item.daily_rate or item_details.daily_rate
            item_map[item.item] = item

    def calculate(self):
        total = 0
        total_qty_rented = 0
        total_qty_returned = 0

        for item in self.items:
            item.daily_rate = flt(item.daily_rate, item.precision("daily_rate"))
            item.days_taken = cint(item.days_taken or 1)
            item.qty = cint(item.qty) or 1
            item.qty_returned = cint(item.qty_returned) or 0

            total_qty_rented += item.qty
            total_qty_returned += item.qty_returned

            item.return_date = add_days(self.date_time, item.days_taken)

            item.amount = flt(
                item.qty *
                item.daily_rate *
                item.days_taken,
                item.precision("amount"))
            total += item.amount

        self.total_qty_rented = total_qty_rented
        self.total_qty_returned = total_qty_returned
        self.total = flt(total, self.precision("total"))
        self.discount = flt(self.discount, self.precision("discount"))
        self.grand_total = flt(self.total - self.discount, self.precision("grand_total"))

    def make_stock_ledger_entries(self):
        target_wh = frappe.get_single("Stock Settings").rented_warehouse
        if not target_wh:
            frappe.throw("Please define Rented Warehouse in Stock Settings")

        from_wh = frappe.db.get_value("Branch", self.branch, "warehouse")
        if not from_wh:
            frappe.throw("Please define Warehouse on Branch")

        sl_entries = []
        for item in self.items:
            item_doc = frappe.get_doc("Item", item.item)
            if not item_doc.is_stock_item:
                frappe.throw("Cannot rent out non-stock item: " + item.name)

            _commons = dict(
                item_code=item.item,
                posting_date=getdate(self.date_time),
                posting_time=get_time(self.date_time),
                doctype=self.doctype,
                name=self.name,
                child_name=item.name,
                docstatus=self.docstatus,
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
        if self.docstatus == 2:
            sl_entries.reverse()

        from erpnext.stock.stock_ledger import make_sl_entries
        make_sl_entries(sl_entries)

    @frappe.whitelist()
    def make_return(self, items):
        items = [frappe._dict(x) for x in items]
        frappe.get_doc(dict(
            doctype="Rental Voucher Event",
            rental_voucher=self.name,
            event_type=RentalVoucherEventType.RETURN.value,
            docstatus=1,
            items=[dict(
                item=x.item, qty=x.qty
            ) for x in items if x.qty > 0]
        )).insert(ignore_permissions=True)

        self.reload()
        return self
