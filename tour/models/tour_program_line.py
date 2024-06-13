from odoo import models, fields, api

class TourProgramLine(models.Model):
    _name = 'tour.program.line'
    _description = 'Tour Program Line'

    product_id = fields.Many2one('product.product', string="Product Name", domain=[('type', '=', 'service')])
    price = fields.Float(string="Price", compute = '_compute_price',readonly=False, store=True)

    tax_id = fields.Many2many(
        comodel_name='account.tax',
        string="Taxes",
        compute='_compute_tax_id',
        store=True, readonly=False,
        )

    tour_id = fields.Many2one('tour.tour', string="Tour Id")
    tax_amount = fields.Float(string='Tax Amount', compute = '_compute_tax')

    @api.depends('tax_id', 'price')
    def _compute_tax(self):
        for rec in self:
            rec.tax_amount = rec._convert_to_tax_base_line_dict()
            print("===================",rec.tax_amount)

    @api.depends('product_id')
    def _compute_price(self):
        for record in self:
            record.price = record.product_id.lst_price

    def _convert_to_tax_base_line_dict(self):
        """ Convert the current record to a dictionary in order to use the generic taxes computation method
        defined on account.tax.

        :return: A python dictionary.
        """
        self.ensure_one()
        tax = self.env['account.tax']._convert_to_tax_base_line_dict(
            self,
            partner=self.env.company.partner_id,
            currency=self.env.company.currency_id,
            product=self.product_id,
            taxes=self.tax_id,
            price_unit=self.price,
            quantity=1,
            discount=0,
            price_subtotal=self.price,
        )
        tax_results = self.env['account.tax']._compute_taxes([tax])
        totals = list(tax_results['totals'].values())[0]
        tax = totals['amount_tax']

        print("tax====================",tax)
        return tax
