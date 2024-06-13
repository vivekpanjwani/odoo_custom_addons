from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    _description = 'Sale Order Line'

    commission_amount = fields.Float(string="Commission Amount", compute="_compute_commission_amount", store=True)
    commission_computed = fields.Boolean(string="Commission Computed", default=False)

    @api.depends('order_id.commission_percentage', 'price_subtotal')
    def _compute_commission_amount(self):
        for line in self:
            if not line.commission_computed:
                if line.price_subtotal and line.order_id.commission_percentage:
                    line.commission_amount = (line.price_subtotal * line.order_id.commission_percentage) / 100
                else:
                    line.commission_amount = 0
                if line.order_id.state == 'sale':
                    line.commission_computed = True
