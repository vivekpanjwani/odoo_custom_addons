from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    zone_id = fields.Many2one('zone.zone', string='Zone', compute='_compute_zone_id', store=True)
    state_id = fields.Many2one('res.country.state', string="State", ondelete='restrict')
    zip = fields.Char(string="Zip")
    
    @api.onchange('state_id', 'zip')
    def _onchange_state_zip(self):
        return {'domain': {'zone_id': [('state_id', '=', self.state_id.id), ('zip_ids.name', '=', self.zip)]}}
    
    @api.depends('zip', 'state_id')
    def _compute_zone_id(self):
        for record in self:
            zone_zip = self.env['zone.zip'].search([('name', '=', record.zip), ('state_id', '=', record.state_id.id)], limit=1)
            record.zone_id = zone_zip.zone_id.id if zone_zip else False

    def _display_address(self, without_company=False):
        address = super(ResPartner, self)._display_address(without_company=without_company)
        if self.zone_id:
            address += "\n%s" % self.zone_id.name
        return address

class ResCountry(models.Model):
    _inherit = 'res.country'

    address_format = fields.Text(default="%(street)s\n%(street2)s\n%(city)s %(state_id)s %(zip)s\n %(zone_id)s\n%(country_id)s")

    