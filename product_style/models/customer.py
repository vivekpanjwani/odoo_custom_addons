from odoo import models, fields

class Customer_rating(models.Model):
    _inherit = 'res.partner'

    rating = fields.Selection([
        ('1', 'Poor'),
        ('2', 'Fair'),
        ('3', 'Good'),
        ('4', 'Very Good'),
        ('5', 'Excellent'),
    ])
