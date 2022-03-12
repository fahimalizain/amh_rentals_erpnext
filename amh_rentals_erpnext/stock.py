import frappe
from frappe.utils import flt
from erpnext import get_default_company
from erpnext.accounts.utils import get_fiscal_year


def get_sl_entry(args):
    args = frappe._dict(args)
    company = get_default_company()

    sl_dict = frappe._dict({
        "item_code": args.item_code,
        "warehouse": args.warehouse,
        "posting_date": args.posting_date,
        "posting_time": args.posting_time,
        'fiscal_year': get_fiscal_year(args.posting_date, company=company)[0],
        "voucher_type": args.doctype,
        "voucher_no": args.name,
        "voucher_detail_no": args.child_name,
        "actual_qty": (args.docstatus == 1 and 1 or -1) * flt(args.stock_qty),
        "stock_uom": frappe.db.get_value("Item", args.get("item_code"), "stock_uom"),
        "incoming_rate": 0,
        "company": company,
        "batch_no": None,
        "serial_no": None,
        "project": None,
        "is_cancelled": 1 if args.docstatus == 2 else 0
    })

    return sl_dict
