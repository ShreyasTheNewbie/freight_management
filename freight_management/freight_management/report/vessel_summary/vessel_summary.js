// Copyright (c) 2025, Shreyas and contributors
// For license information, please see license.txt

frappe.query_reports["Vessel Summary"] = {
	filters: [
        {
            fieldname: "from_date",
            label: "From Date",
            fieldtype: "Date",
            default: frappe.datetime.month_start()
        },
        {
            fieldname: "to_date",
            label: "To Date",
            fieldtype: "Date",
            default: frappe.datetime.month_end()
        },
        {
            fieldname: "shipping_line",
            label: "Shipping Line",
            fieldtype: "Link",
            options: "Shipping Line"
        }
    ]
};
