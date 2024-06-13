from odoo import models, fields, api

class Zone(models.Model):
    _name = 'zone.zone'
    _description = 'Zone Management'

    name = fields.Char(string="Zone Name", required= True)
    code = fields.Char(string="Zone Code", required= True)
    state_id = fields.Many2one('res.country.state', string="State")
    zip_ids = fields.One2many('zone.zip', 'zone_id', string="Zip Codes")
    country_id = fields.Many2one('res.country', string="Country")

    @api.onchange('country_id')
    def _onchange_country_id(self):
        if self.country_id and self.state_id.country_id != self.country_id:
            self.state_id = False

    @api.onchange('state_id')
    def _onchange_state_id(self):
        if self.state_id:
            self.country_id = self.state_id.country_id