from odoo import models, fields

class EmpTag(models.Model):
    _name='emp.tags'
    _description='Employee Tags'

    name = fields.Char("Employee Tag", required=True)
    color = fields.Integer("Color Index")