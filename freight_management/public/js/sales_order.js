frappe.ui.form.on('Sales Order', {
    refresh(frm) {
        if (!frm.doc.__islocal && frm.doc.docstatus === 1 && !frm.doc.custom_shipping_id) {
            frm.add_custom_button(__('Create Direct Shipping'), () => {
            frappe.model.open_mapped_doc({
                    method: 'freight_management.utils.make_direct_shipping',
                    frm: frm
                });
            }, __('Create'));
        }
    }
});

