import frappe


def execute():
    from frappe.utils.fixtures import sync_fixtures
    sync_fixtures()

    for branch in frappe.get_all("Branch"):
        frappe.get_doc("Branch", branch.name).save()
