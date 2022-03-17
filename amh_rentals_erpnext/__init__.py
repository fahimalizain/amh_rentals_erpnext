from enum import Enum


__version__ = '0.0.1'

RENTAL_ITEM_GROUPS = [
    "Centering Items",
    "Event Management Items",
    "Power Tools",
]


class RentalVoucherEventType(Enum):
    RETURN = "Return"
    PAYMENT = "Payment"
    BILL = "Bill"
