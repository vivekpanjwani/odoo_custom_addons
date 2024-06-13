from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    partner_id = fields.Many2one('res.partner')
    zone_id = fields.Many2one('zone.zone', string='Zone', readonly=True, store=True)

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id and self.partner_id.zone_id:
            self.zone_id = self.partner_id.zone_id
        else:
            self.zone_id = False

    