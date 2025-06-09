// Copyright (c) 2025, Shreyas and contributors
// For license information, please see license.txt

frappe.query_reports["Shipping Order Report"] = {
	filters: [
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
            default: "Today",
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
            default: "Today"
        },
        {
            fieldname: "shipping_line",
            label: __("Shipping Line"),
            fieldtype: "Link",
            options: "Shipping Line"
        }
    ]
};
