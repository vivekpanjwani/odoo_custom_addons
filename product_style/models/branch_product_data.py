from odoo import models, fields

class Branch_product_data(models.Model):
    _name = 'branch.product.data'
    _description = 'Branch Product'
    _rec_name='branch_name'

    branch_name=fields.Char(string="Branch Name")
    branch_cost=fields.Float(string="Branch Cost")
    branch_sales_price=fields.Float(string="Branch Sales Price")

    branch_product_id=fields.Many2one('product.template',string="Product Master")

