# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from datetime import date
from odoo.exceptions import ValidationError


class EmployeeModel(models.Model):
    _name = 'employee.employee'
    # _inherit = ['mail.thread', 'mail.activity.mixin']
    _description='Employee Details'
    

    personal_info_id=fields.Integer(string='Personal Info')
    name = fields.Char(string='Name',required=True)
    code=fields.Integer(string='Code',required=True)
    designation_id=fields.Many2one('test_emp.designation',string='Designation')
    blood_group=fields.Selection([('A+', 'A+'),('A-', 'A-'),('B+', 'B+'),('B-', 'B-'),('AB+', 'AB+'),('AB-', 'AB-'),('O+', 'O+'),('O-', 'O-'),],string='Blood Group')
    gender=fields.Selection([('male','Male'),('female','Female'),('other','Other')])
    street = fields.Char(string='Street')
    street2 = fields.Char(string='Street 2')
    city = fields.Char(string='City')
 
    state_id = fields.Many2one('res.country.state', string='State' ,domain="[('country_id', '=', country_id)]")

    zip = fields.Char(string='ZIP')
    country_id = fields.Many2one('res.country', string='Country')

    email=fields.Char(string='Email',store=True ,required=True ,default="abc@gmail.com")
    phone=fields.Char(string='Phone')
    dob=fields.Date(string='DOB')
    age=fields.Float(string='Age',compute='_compute_age')
    marriage_date=fields.Date()
    maritial_status=fields.Selection([('married','Married'),('unmarried','Unmarried'),('divorced','Divorced')])
    signature=fields.Html(string="Signature")
    document=fields.Binary(string='Attached Document')
    tag_ids=fields.Many2many('emp.tags',string='Employee Tags')
    image=fields.Binary(string='Image')
    docs_ids=fields.One2many('doc.doc','employee_id',string='Documents')

    is_manager=fields.Boolean(string='isManager')

    employee_manager_id=fields.Many2one('employee.employee',string='Manager')

    currency_id = fields.Many2one('res.currency', string='Currency')
    salary = fields.Monetary(string='Salary', related='designation_id.salary', currency_field='currency_id', readonly=True)

    contract_id=fields.Many2many('employee.contract', string='Contract')
    
    company_id = fields.Many2one('res.company', string='Company', related="designation_id.company_id",required=True)

    @api.depends('dob')
    def _compute_age(self):
        today = date.today()
        for employee in self:
            if employee.dob:
                dob = fields.Date.from_string(employee.dob)
                employee.age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                if employee.age < 0:
                    raise ValidationError('Age must be Positive')
                if employee.age < 18:
                    raise ValidationError('Age must be more than 18')
            else:
                employee.age = 0
    
    @api.constrains('phone')
    def _check_phone(self):
        for record in self:
            if len(record.phone) != 10:
                raise ValidationError('Phone number must be 10 digits')
            

    @api.onchange('gender','maritial_status')
    def _on_age_warning(self):
        if self.gender=="other":
            return {
                    'warning': {'title': "Warning", 'message': "What is this?", 'type': 'notification'},
                }