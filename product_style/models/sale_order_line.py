from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_new = fields.Many2one('product.style', string="Product Style")

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.product_new = self.product_id.product_style_id