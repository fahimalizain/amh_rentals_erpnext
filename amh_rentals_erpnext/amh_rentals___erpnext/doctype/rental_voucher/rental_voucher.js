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
      {
        label: "Days Taken",
        fieldname: "days_taken",
        fieldtype: "Int",
        reqd: 1,
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
        days_taken: frappe.datetime.get_day_diff(
          frappe.datetime.now_datetime(), frm.doc.date_time
        )
      }));

    const d = new frappe.ui.Dialog({
      title: "Return Items",
      fields: [
        {
          fieldname: "return_date_time",
          fieldtype: "Datetime",
          read_only: 1,
          label: "Current Date Time",
          default: frappe.datetime.now_datetime(),
        },
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

  show_bill_form(frm) {
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
        read_only: 1,
        in_list_view: 1,
      },
      {
        label: "Days Taken",
        fieldname: "days_taken",
        fieldtype: "Int",
        onchange: () => onChange(d),
        reqd: 0,
        in_list_view: 1,
      },
      {
        label: "Daily Rate",
        fieldname: "daily_rate",
        fieldtype: "Currency",
        onchange: () => onChange(d),
        reqd: 0,
        in_list_view: 1,
      },
      {
        label: "Amount",
        fieldname: "amount",
        fieldtype: "Currency",
        read_only: 1,
        in_list_view: 1,
      },
    ];

    const default_rows = frm.doc.items.map((x, idx) => ({
      name: "row " + idx,
      __islocal: true,
      item: x.item,
      qty: x.qty,
      days_taken: x.days_taken,
      daily_rate: x.daily_rate,
      amount: x.amount,
    }));

    const onChange = (d) => {
      let total = 0;
      for (const item of d.get_values().items) {
        item.amount = item.qty * item.days_taken * item.daily_rate;
        total += item.amount;
      }
      d.fields_dict["items"].grid.refresh();
      d.set_value("total", total)
      d.set_value("grand_total", total - d.get_values().discount);
    }

    const d = new frappe.ui.Dialog({
      title: "Finalize Bill",
      fields: [
        {
          fieldname: "items",
          fieldtype: "Table",
          fields: table_fields,
          data: default_rows,
          cannot_add_rows: true,
          cannot_delete_rows: true,
        },
        { fieldtype: "Section Break" },
        {
          fieldname: "total",
          fieldtype: "Currency",
          default: frm.doc.total,
          read_only: 1,
          label: "Total",
        },
        {
          fieldname: "discount",
          fieldtype: "Currency",
          default: frm.doc.discount,
          onchange: () => onChange(d),
          label: "Discount",
        },
        { fieldtype: "Column Break" },
        {
          fieldname: "grand_total",
          fieldtype: "Currency",
          read_only: 1,
          default: frm.doc.grand_total,
          label: "Grand Total",
        },
      ],
      primary_action_label: "Finalize Bill",
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

});
