from odoo import models, fields, api

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    so_id = fields.Many2one('sale.order' , string="Saleorder name")
