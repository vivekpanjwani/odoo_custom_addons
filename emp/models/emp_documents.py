from odoo import models, fields


class Emp_documents(models.Model):
    _name = 'emp.documents'
    _description = 'Documents'

    name = fields.Char(string="Document Name")
    date = fields.Date(string="Date")
    attachment = fields.Binary("Document")
    employee_id = fields.Many2one('emp.model')
