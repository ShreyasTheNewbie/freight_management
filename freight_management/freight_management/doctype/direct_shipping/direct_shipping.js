// Copyright (c) 2025, Shreyas and contributors
// For license information, please see license.txt

frappe.ui.form.on('Direct Shipping', {
    refresh(frm) {
        calculate_total_freight(frm);
        if (frm.doc.workflow_state === "Delivered"){
            frm.disable_form()
        }
    },
    freight_order_line_add(frm) {
        calculate_total_freight(frm);
    },
    freight_order_line_remove(frm) {
        calculate_total_freight(frm);
    }
});

frappe.ui.form.on('Freight Order Line', {
    billing_on: function (frm, cdt, cdn) {
        calculate_total_freight(frm);
    },
    price: function (frm, cdt, cdn) {
        calculate_total_freight(frm);
    },
    volume: function (frm, cdt, cdn) {
        calculate_total_freight(frm);
    },
    gross_weight: function (frm, cdt, cdn) {
        calculate_total_freight(frm);
    }
});

function calculate_total_freight(frm) {
    let total = 0;
    (frm.doc.freight_order_line || []).forEach(row => {
        if (row.billing_on === "Volume" && row.volume && row.price) {
            total += row.volume * row.price;
        } else if (row.billing_on === "Weight" && row.gross_weight && row.price) {
            total += row.gross_weight * row.price;
        } else if (row.price) {
            total += row.price;
        }
    });
    frm.set_value('total_freight', total);
    frm.refresh_field('total_freight');
}
