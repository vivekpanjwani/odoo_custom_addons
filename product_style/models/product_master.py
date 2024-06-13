from odoo import models, fields, api
from datetime import timedelta

class Product_master(models.Model):
    _name="product.template"
    _inherit="product.template"

    product_style_id=fields.Many2one("product.style", string="Product Style")

    business_category_ids = fields.Many2many('product.business', string='Business Categories')
    color=fields.Char(string="Color")

    branch_product=fields.One2many('branch.product.data','branch_product_id')

    last_manufacture_date=fields.Date(string="Last Manufacturing Date")
    new_manufacture_date=fields.Date(string="New Manufacturing Date", compute="_compute_new_manufacture_date")

    
    @api.depends('last_manufacture_date')
    def _compute_new_manufacture_date(self):
        for record in self:
            if record.last_manufacture_date:
                record.new_manufacture_date = fields.Date.to_string(fields.Date.from_string(record.last_manufacture_date) + timedelta(days=7))
            else:
                record.new_manufacture_date = False