from odoo import models, fields

class Emp_contract(models.Model):
    _name = 'emp.contract'
    _description = 'emp.contract'

    name=fields.Char(string="Contract Name")
    from_date = fields.Date(string="From Date")
    to_date=fields.Date(string="To Date")
    emp_cont_id=fields.Many2one('emp.model',string="Employee Contract")