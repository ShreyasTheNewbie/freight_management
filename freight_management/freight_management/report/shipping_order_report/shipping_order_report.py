# Copyright (c) 2025, Shreyas and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart(data)
    return columns, data, None, chart

def get_columns():
    return [
        {"label": _("Name"), "fieldname": "name1", "fieldtype": "Data", "width": 120},
        {"label": _("Source Location"), "fieldname": "source_location", "fieldtype": "Data", "width": 140},
        {"label": _("Destination Location"), "fieldname": "destination_location", "fieldtype": "Data", "width": 140},
        {"label": _("Transport Carriage"), "fieldname": "transport_carriage", "fieldtype": "Data", "width": 130},
        {"label": _("Shipping Line"), "fieldname": "shipping_line", "fieldtype": "Link", "options": "Shipping Line", "width": 120},
        {"label": _("Container No"), "fieldname": "container_no", "fieldtype": "Data", "width": 130},
        {"label": _("20'"), "fieldname": "20", "fieldtype": "Check", "width": 50},
        {"label": _("40'"), "fieldname": "40", "fieldtype": "Check", "width": 50},
        {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
        {"label": _("Remarks"), "fieldname": "remarks", "fieldtype": "Data", "width": 200}
    ]

def get_data(filters):
    direct_shipping_map = {
        d.name: d.order_date for d in frappe.get_all(
            "Direct Shipping", fields=["name", "order_date"])
    }

    data = []
    for d in frappe.get_all("Track Shipping Order", fields=[
        "name1", "source_location", "destination_location", "transport_carriage",
        "shipping_line", "container_no", "`20`", "`40`", "status", "remarks"
    ]):
        order_date = direct_shipping_map.get(d.name1)
        if not order_date:
            continue

        if filters.get("from_date") and order_date < filters["from_date"]:
            continue
        if filters.get("to_date") and order_date > filters["to_date"]:
            continue

        data.append(d)

    return data

def get_chart(data):
    if not data:
        return None

    status_count = {}
    for row in data:
        status = row.get("status") or "Unknown"
        status_count[status] = status_count.get(status, 0) + 1

    return {
        "data": {
            "labels": list(status_count.keys()),
            "datasets": [
                {
                    "name": "Status Count",
                    "values": list(status_count.values())
                }
            ]
        },
        "type": "bar",
        "colors": ["#5e64ff"]
    }
