from odoo import models, fields

class Employee_contract(models.Model):
    _name = 'employee.contract'
    _description='Employee Contract'

    name = fields.Char(string='Name',required=True)
    from_date = fields.Date(string='From Date', required=True)
    to_date = fields.Date(string='To Date', required=True)
    employee_id=fields.Many2one('employee.employee',string='Employee')