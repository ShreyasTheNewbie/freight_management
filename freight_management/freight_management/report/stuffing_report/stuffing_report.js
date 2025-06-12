// Copyright (c) 2025, Shreyas and contributors
// For license information, please see license.txt

frappe.query_reports["Stuffing Report"] = {
	"filters": [
		{
			"fieldname": "date",
			"label": __("Date"),
			"fieldtype": "Date",
		},
		{
			"fieldname": "section",
			"fieldtype": "Select",
			"label": __("Section"),
			"options": [
				{ "value": "Received Goods", "label": __("Received Goods")},
				{ "value": "Stuffed Full Containers", "label": __("Stuffed Full Containers") },
			],
		}
	]
};
