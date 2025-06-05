frappe.ui.form.on('Sales Order', {
    refresh(frm) {
        if (!frm.doc.__islocal && frm.doc.docstatus === 1) {
            frm.add_custom_button(__('Create Direct Shipping'), () => {
                // frappe.call({
                //     method: 'freight_management.utils.get_direct_shipping_data',
                //     args: { sales_order: frm.doc.name },
                //     callback: function (r) {
                //         if (r.message) {
                //             frappe.new_doc('Direct Shipping', r.message);
                //         }
                //     }
                // });
            frappe.model.open_mapped_doc({
                    method: 'freight_management.utils.make_direct_shipping',
                    frm: frm
                });
            }, __('Create'));
        }
    }
});

