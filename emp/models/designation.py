from odoo import models, fields

class Designation(models.Model):
    _name = 'designation.designation'
    _description = 'designation.designation'

    name = fields.Char(string="Designation", required=True)
    currency_id = fields.Many2one('res.currency',string="Currency")
    company = fields.Many2one('res.company',string="Company")
    salary = fields.Monetary(string="Salary", currency_field="currency_id")
    