from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Product_style(models.Model):
    _name = 'product.style'
    _description = 'Product Style'

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True, index=True)

    _sql_constraints = [('unique_code', 'unique(code)', 'Code Must Be Unique !')]
