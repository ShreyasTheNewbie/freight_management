// Copyright (c) 2025, Shreyas and contributors
// For license information, please see license.txt

frappe.query_reports["Daily Activity Report"] = {
	"filters": [
		{
			"fieldname": "date",
			"fieldtype": "Date",
			"label": "Date"
		},
		{
			"fieldname": "user",
			"fieldtype": "Link",
			"label": "User",
			"options": "User"
		}
	]
};
