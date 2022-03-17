// Copyright (c) 2022, Fahim Ali Zain and contributors
// For license information, please see license.txt

frappe.provide("amh_rentals");
amh_rentals.rental_item_groups = [
  "Centering Items",
  "Event Management Items",
  "Power Tools",
];

frappe.ui.form.on("Rental Voucher", {
  refresh: function (frm) {
    if (!frm.doc.date_time) {
      frm.set_value("date_time", frappe.datetime.now_datetime());
    }
    frm.events.calculate(frm);

    frm.set_query("item", "items", () => {
      return {
        filters: {
          item_group: ["in", amh_rentals.rental_item_groups],
        },
      };
    });

    if (frm.doc.docstatus === 1) {
      if (frm.doc.total_qty_rented !== frm.doc.total_qty_returned) {
        frm.add_custom_button(
          "Return",
          () => frm.events.show_return_form(frm),
          "Make"
        );
      } else {
        frm.add_custom_button(
          "Bill",
          () => frm.events.show_bill_form(frm),
          "Make"
        );
      }

      // Outstanding
      if (frm.doc.outstanding_amount > 0) {
        frm.add_custom_button(
          "Payment",
          () => frm.events.show_payment_form(frm),
          "Make"
        );
      }
    }
  },

  calculate(frm) {
    const doc = frm.doc;
    let total = 0;
    for (const item of doc.items) {
      item.daily_rate = flt(item.daily_rate, precision("daily_rate", item));
      item.days_taken = flt(
        item.days_taken || 1,
        precision("days_taken", item)
      );
      if (item.qty <= 0) {
        item.qty = 1;
      } else {
        item.qty = cint(item.qty || 1);
      }

      item.amount = flt(
        item.qty * item.daily_rate * item.days_taken,
        precision("amount", item)
      );

      item.return_date = frappe.datetime.add_days(
        doc.date_time,
        item.days_taken
      );
      total += item.amount;
    }
    total = flt(total, precision("total"));
    doc.total = total;

    doc.discount = flt(doc.discount, precision("discount"));
    doc.grand_total = flt(doc.total - doc.discount, precision("grand_total"));
    frm.refresh_fields();
  },

  discount(frm) {
    frm.events.calculate(frm);
  },

  show_return_form(frm) {
    const table_fields = [
      {
        label: "Item",
        fieldtype: "Link",
        fieldname: "item",
        options: "Item",
        reqd: 1,
        in_list_view: 1,
        read_only: 1,
      },
      {
        label: "Qty",
        fieldname: "qty",
        fieldtype: "Int",
        reqd: 0,
        in_list_view: 1,
      },
    ];

    const default_rows = frm.doc.items
      .filter((x) => x.qty > x.qty_returned)
      .map((x, idx) => ({
        name: "row " + idx,
        __islocal: true,
        item: x.item,
        qty: x.qty - x.qty_returned,
      }));

    const d = new frappe.ui.Dialog({
      title: "Return Items",
      fields: [
        {
          fieldname: "items",
          fieldtype: "Table",
          fields: table_fields,
          data: default_rows,
          cannot_add_rows: true,
          cannot_delete_rows: true,
        },
      ],
      primary_action_label: "Make Return",
      primary_action(values) {
        frm.call({
          method: "make_return",
          args: values,
          doc: frm.doc,
          callback(r) {
            if (r.exc) {
              frappe.msgprint("Something went wrong! Please contact developer");
            } else {
              frappe.msgprint("Return made successfully");
              d.hide();
            }
          },
        });
      },
    });
    d.show();
  },
});

frappe.ui.form.on("Rental Voucher Item", {
  daily_rate(frm, cdt, cdn) {
    frm.events.calculate(frm);
  },
  days_taken(frm, cdt, cdn) {
    frm.events.calculate(frm);
  },
  qty(frm, cdt, cdn) {
    frm.events.calculate(frm);
  },
  items_add(frm, cdt, cdn) {
    frm.events.calculate(frm);
  },
  items_remove(frm, cdt, cdn) {
    frm.events.calculate(frm);
  },
  days_taken(frm, cdt, cdn) {
    frm.events.calculate(frm);
  },
});
