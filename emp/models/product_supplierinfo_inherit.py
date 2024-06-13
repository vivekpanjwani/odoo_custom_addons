from odoo import models, fields, api

class ProductSupplierInfo(models.Model):
    _inherit = 'product.supplierinfo'

    def open_po(self):
        PurchaseOrder = self.env['purchase.order']
        PurchaseOrderLine = self.env['purchase.order.line']

        po_line_ids = PurchaseOrderLine.search([('product_id.product_tmpl_id', '=', self.product_tmpl_id.id)]).ids
        po_order = PurchaseOrder.search([('partner_id', '=', self.partner_id.id), ('order_line', 'in', po_line_ids)], order='date_approve desc', limit=3)

        action = self.env.ref('purchase.purchase_rfq').read()[0]
        action['domain'] = [('id', 'in', po_order.ids)]
        return action
    