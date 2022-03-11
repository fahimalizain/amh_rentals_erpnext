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
      item.amount = flt(
        item.daily_rate * item.days_taken,
        precision("amount", item)
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
});

frappe.ui.form.on("Rental Voucher Item", {
  daily_rate(frm, cdt, cdn) {
    frm.events.calculate(frm);
  },
  days_taken(frm, cdt, cdn) {
    frm.events.calculate(frm);
  },
  items_add(frm, cdt, cdn) {
    frm.events.calculate(frm);
  },
  items_remove(frm, cdt, cdn) {
    frm.events.calculate(frm);
  },
});
