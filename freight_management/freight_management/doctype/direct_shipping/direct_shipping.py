# Copyright (c) 2025, Shreyas and contributors
# For license information, please see license.txt

import frappe
from frappe import msgprint, _
from frappe.model.document import Document
from erpnext.selling.doctype.sales_order.sales_order import make_delivery_note
from frappe.utils import  get_link_to_form

class DirectShipping(Document):
	def after_insert(self):
		if self.sales_order:
			frappe.db.set_value("Sales Order", self.sales_order, "custom_shipping_id", self.name,update_modified=False)
	def on_trash(self):
		frappe.db.delete("Track Shipping Order", {"name1": self.name})
		frappe.db.set_value("Sales Order", self.sales_order, "custom_shipping_id", None,update_modified=False) 

def validate(self,cdt):
	for c in self.containers:
		if c.container_no:
			if not frappe.db.exists("Track Shipping Order",{"container_no":c.container_no,"name1":self.name, "row_name":c.name}):
				vals = frappe.get_doc({
				"doctype": "Track Shipping Order",
				"name1":self.name,
				"source_location":self.loading_port,
				"destination_location":self.discharging_port,
				"transport_carriage":self.transport,
				"container_no":c.container_no,
				"20":c.get('20'),
				"40":c.get('40'),
				"shipping_line":self.shipping_line,
				"status":self.workflow_state,
				"row_name":c.name
				})
				vals.save()
			else:
				test_doc = frappe.get_doc("Track Shipping Order",{"container_no":c.container_no,"name1":self.name})
				test_doc.source_location = self.loading_port
				test_doc.destination_location = self.discharging_port
				test_doc.transport_carriage = self.transport
				test_doc.container_no = c.container_no
				test_doc.shipping_line = self.shipping_line
				test_doc.name1 = self.name
				test_doc.set("20",c.get('20'))
				test_doc.set("40",c.get('40'))
				test_doc.status = self.workflow_state
				test_doc.row_name = c.name
				test_doc.save()
	# else:
	# 	vals = frappe.get_doc({
	# 		"doctype": "Track Shipping Order",
	# 		"name1":self.name,
	# 		"source_location":self.loading_port,
	# 		"destination_location":self.discharging_port,
	# 		"transport_carriage":self.transport,
	# 		"status":self.workflow_state
	# 		})
	# 	vals.save()
	old_doc = self.get_doc_before_save()
	if old_doc and old_doc.workflow_state != self.workflow_state:
		if self.workflow_state == "Delivered":
			doc = make_delivery_note(self)
			doc.save()
			msgprint(_("Delivery Note <b>{0} </b>created successfully.<br> Please submit It").format(get_link_to_form("Delivery Note",doc.name)))

@frappe.whitelist()
def add_containers_to_track_shipping_order(doc, method):
	"""
	Add containers to Track Shipping Order if not already present.
	"""
	if doc.sales_order:

		commodity = frappe.get_value("Sales Order", doc.sales_order, "custom_commodity")
		if commodity :
			a  = frappe.db.get_value("Sales Order", doc.sales_order, "custom_20")
			b = frappe.db.get_value("Sales Order", doc.sales_order, "custom_40")
			if a:
				for i in range(a):
					doc.append("containers", {
						"20": 1
					})
			if b:
				for i in range(b):
					doc.append("containers", {
						"40": 1
					})