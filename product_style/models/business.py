from odoo import models, fields

class Product_Business(models.Model):
    _name = 'product.business'
    _description = 'Business'

    name=fields.Char(string="Business Category")
