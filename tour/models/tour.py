from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Tour(models.Model):
    _name = 'tour.tour'
    _description = 'Tour'

    name = fields.Char()
    email = fields.Char(string="Customer Email", required=True)
    phone = fields.Char(string="Customer Phone")

    enquiry_code = fields.Char(string="Customer Enquiry", readonly=True)

    tour_name = fields.Many2one('tour.package', string = "Tour Name")
    package_price = fields.Float(related="tour_name.package_price", string="Package Price")

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date", required=True)

    tour_program = fields.One2many('tour.program.line', 'tour_id', string="Tour Program")

    taxes = fields.Float(compute="compute_all_taxes",string="Tax")
    subtotal = fields.Float(string="Subtotal" , compute = 'compute_subtotal')
    final_total =fields.Float(string="Final", compute='compute_finaltotal')

    @api.onchange('end_date')
    def end_date_check(self):
        for record in self:
            if record.start_date > record.end_date:
                raise ValidationError("End Date should be greater than Start Date")
            
    def name_get(self):
            result = []
            for record in self:
                name = f"{record.enquiry_code}"
                result.append((record.id, name))
            return result

    @api.model_create_multi
    def create(self, vals_list):
        print("#################################### ")
        
        for vals in vals_list:
            if self.search([('enquiry_code', '=', vals.get('enquiry_code'))]):
               vals['enquiry_code'] = self.env['ir.sequence'].next_by_code('tour.tour')
                
            if vals.get('enquiry_code', _("New")) == _("New"):
                seq_date = fields.Datetime.context_timestamp(
                    self, fields.Datetime.to_datetime(vals['date_time'])
                ) if 'date_time' in vals else None
                vals['enquiry_code'] = self.env['ir.sequence'].next_by_code(
                    'tour.tour', sequence_date=seq_date) or _("New")
                
        res = super().create(vals_list)
        print(res)
        return res

    @api.depends('tour_program.price')
    def compute_subtotal(self):
        for record in self:
            record.subtotal = sum(i.price for i in record.tour_program)

    @api.depends('taxes','subtotal')
    def compute_finaltotal(self):
        for record in self:
            record.final_total = record.taxes + record.subtotal

    @api.depends('tour_program.tax_amount')
    def compute_all_taxes(self):
        for record in self:
            record.taxes = sum(i.tax_amount for i in record.tour_program)