import frappe
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def make_direct_shipping(source_name):

    target = get_mapped_doc(
        "Sales Order",
        source_name,
        {
            "Sales Order": {
                "doctype": "Direct Shipping",
                "field_map": {
                    "name": "sales_order",
                    "transaction_date": "order_date",
                    "customer": "customer",
                    "company": "company",
                    "customer_name": "party",
                    "custom_local__transit": "local__transit"
                }
            }
        },
        None
    )

    return target
