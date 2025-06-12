# Copyright (c) 2025, Shreyas and contributors
# For license information, please see license.txt

import frappe
def execute(filters=None):
    from frappe import _
    from frappe.utils import getdate

    # Define columns based on selected section
    if not filters or not filters.get("section"):
        return [], []

    date_filter = filters.get("date")
    section = filters.get("section")

    if section == "Received Goods":
        columns = [
            {"label": _("Truck No"), "fieldname": "truck_no", "fieldtype": "Data", "width": 150},
            {"label": _("Trailer No"), "fieldname": "trailer_no", "fieldtype": "Data", "width": 150},
            {"label": _("Bags"), "fieldname": "bags", "fieldtype": "Int", "width": 100},
            {"label": _("Full Load"), "fieldname": "full_load", "fieldtype": "Int", "width": 100},
            {"label": _("Less"), "fieldname": "less", "fieldtype": "Data", "width": 100},
            {"label": _("More"), "fieldname": "more", "fieldtype": "Data", "width": 100},
            {"label": _("Remarks"), "fieldname": "remarks", "fieldtype": "Small Text", "width": 400},
        ]
        data_source = """
            SELECT
                rg.truck_no, rg.trailer_no, rg.bags, rg.full_load,
                rg.less, rg.more, rg.remarks
            FROM
                `tabStuffing Details` sd
            LEFT JOIN
                `tabReceived Goods` rg ON sd.name = rg.parent
            WHERE
                sd.date = %(date)s AND rg.parent IS NOT NULL
        """

    elif section == "Stuffed Full Containers":
        columns = [
            {"label": _("Container No"), "fieldname": "container_no", "fieldtype": "Data", "width": 150},
            {"label": _("Quantity"), "fieldname": "quantity", "fieldtype": "Int", "width": 100},
            {"label": _("Shipping Line"), "fieldname": "shipping_line_sea__line", "fieldtype": "Data", "width": 150},
            {"label": _("Customs Seal"), "fieldname": "customs_seal", "fieldtype": "Data", "width": 150},
            {"label": _("Destination"), "fieldname": "destination", "fieldtype": "Data", "width": 150},
            {"label": _("Remarks"), "fieldname": "remarks", "fieldtype": "Small Text", "width": 400},
        ]
        data_source = """
            SELECT
                fc.container_no, fc.quantity, fc.shipping_line_sea__line,
                fc.customs_seal, fc.destination, fc.remarks
            FROM
                `tabStuffing Details` sd
            LEFT JOIN
                `tabStuffed Full Containers` fc ON sd.name = fc.parent
            WHERE
                sd.date = %(date)s AND fc.parent IS NOT NULL
        """

    else:
        return [], []


    data = frappe.db.sql(data_source, {"date": date_filter}, as_dict=1)

    return columns, data