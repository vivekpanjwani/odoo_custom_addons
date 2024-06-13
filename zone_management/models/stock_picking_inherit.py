from odoo import models, fields

class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    zone_id = fields.Many2one(related='partner_id.zone_id', string='Zone', store=True, readonly=True)