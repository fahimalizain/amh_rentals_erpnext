import frappe


def on_update(doc, method=None):
    make_warehouse(doc)


def make_warehouse(doc):
    if doc.warehouse:
        return

    common_parent = frappe.db.get_value("Warehouse", {"is_group": 0}, ["parent_warehouse"])

    d = frappe.get_doc(frappe._dict(
        doctype="Warehouse",
        warehouse_name=doc.name,
        parent_warehouse=common_parent,
    )).insert(ignore_permissions=True)

    doc.db_set("warehouse", d.name)
