from odoo import models, fields, api

class Tour_package(models.Model):
    _name = 'tour.package'
    _description = 'Tour Package'

    name = fields.Char("Tour Package")

    type = fields.Selection([
        ('fixed','Fixed'),
        ('custom', 'Custom'),
    ], string="Type")
    package_price = fields.Float(string="Package Price")
    days = fields.Float(string="No. of days")
    final_price = fields.Float("Final Price", compute='_compute_final_price')

    @api.depends('type', 'package_price', 'days')
    def _compute_final_price(self):
        for record in self:
            if record.type == 'custom':
                record.final_price = record.days * record.package_price
            elif record.type == 'fixed':
                record.final_price = record.package_price
            else:
                record.final_price = 0.0