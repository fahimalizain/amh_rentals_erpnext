# Copyright (c) 2022, Fahim Ali Zain and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt, cint

from amh_rentals_erpnext import RENTAL_ITEM_GROUPS


class RentalVoucher(Document):
    def validate(self):
        self.validate_items()
        self.calculate()

    def validate_items(self):
        for item in self.items:
            item_details = frappe.db.get_value(
                "Item", item.item, ["name", "item_group", "daily_rate"], as_dict=1)

            if item_details.item_group not in RENTAL_ITEM_GROUPS:
                frappe.throw("Non-Rentable Item")

            item.daily_rate = item_details.daily_rate

    def calculate(self):
        total = 0
        for item in self.items:
            item.daily_rate = flt(item.daily_rate, item.precision("daily_rate"))
            item.days_taken = cint(item.days_taken or 1)
            item.amount = flt(item.daily_rate * item.days_taken, item.precision("amount"))
            total += item.amount

        self.total = flt(total, self.precision("total"))
        self.discount = flt(self.discount, self.precision("discount"))
        self.grand_total = flt(self.total - self.discount, self.precision("grand_total"))
