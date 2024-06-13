from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    rating = fields.Selection(related='partner_id.rating', string="Customer Rating", readonly=True)