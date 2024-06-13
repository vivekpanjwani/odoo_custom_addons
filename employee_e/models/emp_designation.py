from odoo import models, fields

class EmpDesignation(models.Model):
    _name = 'test_emp.designation'
    _description = 'Employee Designation'

    name = fields.Char(string='Designation Name', required=True)
    company_id = fields.Many2one('res.company', string='Company',default=lambda self: self.env.company, required=True)
    currency_id = fields.Many2one('res.currency', string='Currency')
    salary = fields.Monetary(string='Salary', currency_field='currency_id')