// Copyright (c) 2025, Shreyas and contributors
// For license information, please see license.txt

frappe.ui.form.on('Direct Shipping', {
    refresh(frm) {
        if (frm.doc.workflow_state === "Delivered") {
            frm.disable_form()
        }
        frm.trigger("show_progress_for_tracking_orders");
        frm.toggle_reqd(["loading_port", "discharging_port", "shipping_line"], 1)
        frm.fields_dict.containers.grid.update_docfield_property("container_no", "reqd", 1)
        frm.set_df_property('containers', 'cannot_add_rows', true);
        frm.set_df_property('containers', 'cannot_delete_rows', true);
        frm.set_df_property('containers', 'cannot_delete_all_rows', true);
    },
    before_workflow_action: function (frm) {
        if (frm.doc.docstatus !== 1) {
            check_mandatory_fields(frm)
        }
    },
    show_progress_for_tracking_orders(frm) {
        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: "Track Shipping Order",
                fields: ["status", "name"],
                filters: {
                    name1: frm.doc.name
                },
                limit_page_length: 100
            },
            callback(r) {
                if (!r.message || !r.message.length) return;

                let status_order = [
                    "Draft",
                    "Approved",
                    "In Progress",
                    "In Transit",
                    "Received",
                    "Delivered",
                    "Pending",
                    "Rejected"
                ];

                let status_colors = {
                    "Draft": "progress-bar-warning",  // updated
                    "Approved": "progress-bar-info",
                    "In Progress": "progress-bar-warning",
                    "In Transit": "progress-bar-warning",  // custom class
                    "Received": "progress-bar-success",
                    "Delivered": "progress-bar-success",
                    "Pending": "progress-bar-muted",
                    "Rejected": "progress-bar-danger"
                };

                let total = r.message.length;
                let status_map = {};

                for (let row of r.message) {
                    let status = row.status || "Unknown";
                    if (!status_map[status]) {
                        status_map[status] = [];
                    }
                    status_map[status].push(row.name);
                }

                let bars = [];
                let message = "";

                for (let status of status_order) {
                    if (status_map[status]) {
                        let count = status_map[status].length;
                        let percent = (count / total) * 100;
                        let names_list = status_map[status].join(", ");
                        bars.push({
                            title: `${count} ${status} (${names_list})`,
                            width: percent + "%",
                            progress_class: status_colors[status] || "progress-bar-info"
                        });
                        message += `<b>${status}</b>: ${names_list}. `;
                    }
                }

                frm.dashboard.add_progress(__("Shipping Status"), bars, message);
            }
        });
    }

});


function check_mandatory_fields(frm) {
    let has_errors = false;
    frm.scroll_set = false;

    if (frm.doc.docstatus === 2) return true; // don't check on cancel

    $.each(frappe.model.get_all_docs(frm.doc), function (i, doc) {
        let error_fields = [];
        let folded = false;

        $.each(frappe.meta.docfield_list[doc.doctype] || [], function (i, docfield) {
            if (docfield.fieldname) {
                const df = frappe.meta.get_docfield(doc.doctype, docfield.fieldname, doc.name);

                if (df.fieldtype === "Fold") folded = frm.layout.folded;

                if (is_mandatory(doc, df) && !frappe.model.has_value(doc.doctype, doc.name, df.fieldname)) {
                    has_errors = true;
                    error_fields.push(__(df.label, null, df.parent));
                    if (!frm.scroll_set) {
                        frm.scroll_to_field(doc.parentfield || df.fieldname);
                        frm.scroll_set = true;
                    }
                    if (folded) {
                        frm.layout.unfold();
                        folded = false;
                    }
                }
            }
        });

        if (error_fields.length) {
            let meta = frappe.get_meta(doc.doctype);
            let message = __("Mandatory fields required in {0}", [__(doc.doctype)]);
            message += "<br><br><ul><li>" + error_fields.join("</li><li>") + "</li></ul>";
            frappe.dom.unfreeze()
            frappe.throw({ title: __("Missing Fields"), message: message });

            frm.refresh();
        }
    });

    return !has_errors;
}

function is_mandatory(doc, df) {
    if (df.reqd) return true;
    if (!df.mandatory_depends_on || !doc) return false;

    const expression = df.mandatory_depends_on;
    let out;

    if (typeof expression === "boolean") {
        out = expression;
    } else if (typeof expression === "function") {
        out = expression(doc);
    } else if (expression.substr(0, 5) === "eval:") {
        try {
            out = frappe.utils.eval(expression.substr(5), { doc });
        } catch (e) {
            frappe.throw(__('Invalid "mandatory_depends_on" expression'));
        }
    } else {
        out = !!doc[expression];
    }

    return out;
}


const scroll_to = (fieldname) => {
    frm.scroll_to_field(fieldname);
    frm.scroll_set = true;
};