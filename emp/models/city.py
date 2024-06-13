from odoo import models, fields, api
from odoo.osv import expression

class City(models.Model):
    _name = 'city.city'
    _description = 'Cities'

    name = fields.Char(string="City Name")
    state_ids = fields.Many2one('res.country.state', string="State")

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = [('name', operator, name.strip())] if name and name.strip() else []
        if self.env.context.get('state_id'):
            domain = expression.AND([args, [('state_ids', '=', self.env.context.get('state_id'))], domain])
        return self._search(domain, limit=limit, access_rights_uid=name_get_uid)