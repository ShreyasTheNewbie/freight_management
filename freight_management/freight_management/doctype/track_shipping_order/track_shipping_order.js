// Copyright (c) 2025, Shreyas and contributors
// For license information, please see license.txt

frappe.ui.form.on('Track Shipping Order', {
    refresh(frm) {
		frm.toggle_enable(["name1", "status", "remarks", "shipping_line", "source_location", "destination_location", "transport_carriage"], 0);
        if (frm.doc.status !== "Delivered" && !frm.is_new()) {
            frm.add_custom_button(__('Update Status'), () => {
                let dialog = new frappe.ui.Dialog({
                    title: 'Update Shipping Status',
                    fields: [
                        {
                            label: 'New Status',
                            fieldname: 'new_status',
                            fieldtype: 'Select',
                            options: [
                                'Draft',
                                'Approved',
                                'In Progress',
                                'In Transit',
                                'Received',
                                'Delivered',
                                'Pending',
                                'Rejected'
                            ],
                            reqd: 1,
							"default": frm.doc.status || 'Delivered'

                        },
                        {
                            label: 'Remarks',
                            fieldname: 'remarks',
                            fieldtype: 'Small Text'
                        }
                    ],
                    primary_action_label: 'Update',
                    primary_action(values) {
                        frm.set_value('status', values.new_status);
                        frm.set_value('remarks', values.remarks || '');
                        frm.save();
                        dialog.hide();
                    }
                });
                dialog.show();
            });
        }
    }
});
