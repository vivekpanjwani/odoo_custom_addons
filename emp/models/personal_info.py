from odoo import models, fields

class Emp_personal_info(models.Model):
    _name = 'emp.personal.info'
    _description = 'Personal Info'
    _inherits = {'emp.model': 'emp_id'}

    emp_id = fields.Many2one('emp.model', ondelete='cascade', required=True)
    