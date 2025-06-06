# Copyright (c) 2025, Shreyas and contributors
# For license information, please see license.txt

import frappe
from frappe import msgprint, _
from frappe.model.document import Document
from erpnext.selling.doctype.sales_order.sales_order import make_delivery_note
from frappe.utils import  get_link_to_form

class DirectShipping(Document):
	pass

def validate(self,cdt):
	for d in self.get('freight_order_line'):
		if d.pricing:
			if d.billing_on == "Volume":
				d.sale_price = d.volume * d.price
			else:
				d.sale_price = d.gross_weight * d.price
	test_d = frappe.db.get_value("Track Shipping Order",{'name1':self.name},'name')
	if test_d:
		test_doc = frappe.get_doc("Track Shipping Order",test_d)
		test_doc.source_location = self.loading_port
		test_doc.destination_location = self.discharging_port
		test_doc.transport_carriage = self.transport
		test_doc.status = self.workflow_state
		test_doc.save()
	else:
		vals = frappe.get_doc({
			"doctype": "Track Shipping Order",
			"name1":self.name,
			"source_location":self.loading_port,
			"destination_location":self.discharging_port,
			"transport_carriage":self.transport,
			"status":self.workflow_state
			})
		vals.save()
	old_doc = self.get_doc_before_save()
	if old_doc and old_doc.workflow_state != self.workflow_state:
		if self.workflow_state == "Delivered":
			doc = make_delivery_note(self)
			doc.save()
			msgprint(_("Delivery Note <b>{0} </b>created successfully.<br> Please submit It").format(get_link_to_form("Delivery Note",doc.name)))