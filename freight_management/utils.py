import frappe
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def make_direct_shipping(source_name):
    return get_mapped_doc(
        "Sales Order", source_name,
        {
            "Sales Order": {
                "doctype": "Direct Shipping",
                "field_map": {
                    "name": "sales_order",
                    "transaction_date": "order_date",
                    "customer": "customer",
                    "company": "company",
                    "customer_name": "party"
                }
            },
            "Sales Order Item": {
                "doctype": "Freight Order Line",
                "field_map": {
                    "item_code": "items",
                    "rate": "price",
                    "amount": "sale_price"
                }
            }
        },
        target_doc=None  # do not save
    )
