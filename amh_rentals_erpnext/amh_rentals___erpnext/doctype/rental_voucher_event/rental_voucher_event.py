# Copyright (c) 2022, Fahim Ali Zain and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from frappe.utils import now

from amh_rentals_erpnext import RentalVoucherEventType


class RentalVoucherEvent(Document):
    def validate(self):
        if not self.date_time:
            self.date_time = now()

    def on_submit(self):
        _type = RentalVoucherEventType(self.event_type)
        _handler = None
        if _type == RentalVoucherEventType.RETURN:
            from .handlers.make_return import up
            _handler = up

        if _handler:
            _handler(event=self)

    def on_cancel(self):
        self.ignore_linked_doctypes = ('GL Entry', 'Stock Ledger Entry', 'Repost Item Valuation')

        _type = RentalVoucherEventType(self.event_type)
        _handler = None
        if _type == RentalVoucherEventType.RETURN:
            from .handlers.make_return import down
            _handler = down

        if _handler:
            _handler(event=self)
