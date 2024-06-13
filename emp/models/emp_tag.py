from odoo import models, fields
from random import randint


class Emp_Tag(models.Model):
    _name = 'emp.tag'
    _description = 'Employee Tags'


    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char(string="Employee Tag")
    color = fields.Integer(string='Color Index', default=_get_default_color)
    employee_ids = fields.Many2many('emp.model', 'employee_tag_rel', 'tag_id', 'emp_id', string='Employees')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]

    