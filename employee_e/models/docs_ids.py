from odoo import models, fields, api


class Doc_id(models.Model):
    _name = 'doc.doc'
    _description='Documents Details'

    name = fields.Char(string='Name',required=True)
    date=fields.Date(string='Date') 
    attached_ids = fields.Binary(string='Attached Documents')
    employee_id=fields.Many2one('employee.employee')