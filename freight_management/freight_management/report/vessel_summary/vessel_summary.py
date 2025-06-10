# Copyright (c) 2025, Shreyas and contributors
# For license information, please see license.txt


import frappe
from frappe import _
from frappe.utils import getdate

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": _("Vessel Name"), "fieldname": "name1", "fieldtype": "Data", "width": 150},
        {"label": _("Shipping Line"), "fieldname": "shipping_line", "fieldtype": "Link", "options": "Shipping Line", "width": 120},
        {"label": _("Draft (m)"), "fieldname": "draft", "fieldtype": "Float", "width": 100},
        {"label": _("LOA"), "fieldname": "loa", "fieldtype": "Float", "width": 100},
        {"label": _("GRT"), "fieldname": "grt", "fieldtype": "Float", "width": 100},
        {"label": _("ETA"), "fieldname": "eta", "fieldtype": "Datetime", "width": 140},
        {"label": _("ETB"), "fieldname": "etb", "fieldtype": "Datetime", "width": 140},
        {"label": _("ETD"), "fieldname": "etd", "fieldtype": "Datetime", "width": 140},
        {"label": _("Discharge 20'"), "fieldname": "discharge_20", "fieldtype": "Int", "width": 110},
        {"label": _("Discharge 40'"), "fieldname": "discharge_40", "fieldtype": "Int", "width": 110},
        {"label": _("Load 20'"), "fieldname": "load_20", "fieldtype": "Int", "width": 100},
        {"label": _("Load 40'"), "fieldname": "load_40", "fieldtype": "Int", "width": 100},
        {"label": _("Remarks"), "fieldname": "remarks", "fieldtype": "Data", "width": 200}
    ]

def get_data(filters):
    conditions = []
    if filters:
        if filters.get("from_date"):
            conditions.append(["eta", ">=", getdate(filters["from_date"])])
        if filters.get("to_date"):
            conditions.append(["eta", "<=", getdate(filters["to_date"])])
        if filters.get("shipping_line"):
            conditions.append(["shipping_line", "=", filters["shipping_line"]])

    return frappe.get_all("Vessels",
        filters=conditions,
        fields=[
            "name1", "shipping_line", "draft", "loa", "grt",
            "eta", "etb", "etd", "discharge_20", "discharge_40",
            "load_20", "load_40", "remarks"
        ]
    )
