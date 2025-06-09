# Copyright (c) 2025, Shreyas and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart(data)
    # message = get_progress_message(data)
    return columns, data, None, chart

def get_columns():
    return [
        {"label": _("Booking ID"), "fieldname": "booking_id", "fieldtype": "Data", "width": 130},
        {"label": _("Shipping ID"), "fieldname": "name1", "fieldtype": "Data", "width": 120},
        {"label": _("Source Location"), "fieldname": "source_location", "fieldtype": "Data", "width": 140},
        {"label": _("Destination Location"), "fieldname": "destination_location", "fieldtype": "Data", "width": 140},
        {"label": _("Shipping Line"), "fieldname": "shipping_line", "fieldtype": "Link", "options": "Shipping Line", "width": 120},
        {"label": _("Container No"), "fieldname": "container_no", "fieldtype": "Data", "width": 130},
        {"label": _("20'"), "fieldname": "20", "fieldtype": "Check", "width": 50},
        {"label": _("40'"), "fieldname": "40", "fieldtype": "Check", "width": 50},
        {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
        {"label": _("Remarks"), "fieldname": "remarks", "fieldtype": "Data", "width": 200}
    ]

def get_data(filters):
    from_date = getdate(filters.get("from_date")) if filters.get("from_date") else None
    to_date = getdate(filters.get("to_date")) if filters.get("to_date") else None

    direct_shipping_map = {
        d.name: getdate(d.order_date) for d in frappe.get_all(
            "Direct Shipping", fields=["name", "order_date"])
    }

    data = []
    for d in frappe.get_all("Track Shipping Order", fields=[
        "name1", "source_location", "destination_location", "transport_carriage",
        "shipping_line", "container_no", "`20`", "`40`", "status", "remarks"
    ]):
        order_date = direct_shipping_map.get(d.name1)
        d["booking_id"] = frappe.bold(frappe.db.get_value("Direct Shipping",d.name1,"name1 as booking_id"))
        
        d["name1"] = d.name1
        if not order_date:
            continue

        if from_date and order_date < from_date:
            continue
        if to_date and order_date > to_date:
            continue
            
        data.append(d)

    return data

def get_chart(data):
    if not data:
        return None

    status_count = {}
    color_map = {
        "Draft": "#f0ad4e",
        "Approved": "#5bc0de",
        "In Progress": "#ffcc00",
        "In Transit": "#9370db",
        "Received": "#5cb85c",
        "Delivered": "#4caf50",
        "Pending": "#999999",
        "Rejected": "#d9534f",
        "Unknown": "#777777"
    }

    for row in data:
        status = (row.get("status") or "Unknown").strip()
        status_count[status] = status_count.get(status, 0) + 1

    labels = list(status_count.keys())
    values = [status_count[status] for status in labels]
    colors = [color_map.get(status, "#5e64ff") for status in labels]

    return {
        "data": {
            "labels": labels,
            "datasets": [
                {
                    "name": "Status Count",
                    "values": values
                }
            ]
        },
        "type": "donut",
        "colors": colors
    }

def get_progress_message(data):
    status_map = {}
    for row in data:
        status = (row.get("status") or "Unknown").strip()
        status_map.setdefault(status, []).append(row.get("name1"))

    lines = []
    for status, names in status_map.items():
        lines.append(f"{status}: {', '.join(names)}")

    return " | ".join(lines)

