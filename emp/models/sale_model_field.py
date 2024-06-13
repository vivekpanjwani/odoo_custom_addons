from odoo import models, fields

class Emp_sale_model_field(models.Model):
    _inherit = "sale.order.line"
    _descirption = "New Field"

    extra_field = fields.Boolean()