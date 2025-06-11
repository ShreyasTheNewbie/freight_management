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
        {"label": _("Date"), "fieldname": "date", "fieldtype": "Date", "width": 150},
        {"label": _("User"), "fieldname": "user", "fieldtype": "Link", "options": "User", "width": 150},
        {"label": _("Location"), "fieldname": "location", "fieldtype": "Data", "width": 350},
        {"label": _("Activites"), "fieldname": "activites", "fieldtype": "Data", "width": 400},
        {"label": _("Result / Expected"), "fieldname": "result__expected", "fieldtype": "Data", "width": 400},
        {"label": _("Remarks"), "fieldname": "remarks", "fieldtype": "Data", "width": 400},
    ]

def get_data(filters):
    conditions = {}

    if filters.get("date"):
        conditions["date"] = filters["date"]
    if filters.get("user"):
        conditions["user"] = filters["user"]

    records = frappe.get_all(
        "Daily Activity",
        fields=["date", "user", "location", "activites", "result__expected", "remarks","name"],
        filters=conditions,
        order_by="date desc"
    )
    return records
