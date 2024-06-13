from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ZoneZip(models.Model):
    _name = 'zone.zip'
    _description = 'Zone Zip Codes'

    name = fields.Char(string="Zip", required=True)
    zone_id = fields.Many2one('zone.zone', string="Zone")
    state_id = fields.Many2one('res.country.state', string="State", store=True)

    @api.constrains('name', 'state_id')
    def _check_zip(self):
        for record in self:
            if self.env['zone.zip'].search([('name', '=', record.name), ('state_id', '=', record.state_id.id), ('id', '!=', record.id)], limit=1):
                raise ValidationError("The zip code already exists in the same state.")
            