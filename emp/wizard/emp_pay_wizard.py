from odoo import models, fields,api
from odoo.exceptions import UserError
from datetime import datetime,timedelta

class EmpPayWizard(models.TransientModel):
    _name = 'emp.pay.wizard'
    _description = 'Employee Wizard'

    partner_id = fields.Many2one("res.partner",string='Partner')
    basic_salary = fields.Float(string="Basic Salary")
    from_date = fields.Date(string="From Date", required=True)
    to_date = fields.Date(string="To Date", required=True)
    net_salary = fields.Float(string="Net Salary")
    gross_salary = fields.Float(string="Gross Salary")
    commision = fields.Integer(string="Commision")
    extra_allowances=fields.Float(string="Extra Allowances")

    emp_id = fields.Many2one('emp.model', string='Employee')


    @api.model
    def default_get(self, fields):
        res = super(EmpPayWizard, self).default_get(fields)
        emp_id = self.env.context.get('active_id')
        if emp_id:
            emp_record = self.env['emp.model'].browse(emp_id)
            if emp_record:
                if 'partner_id' in fields:
                    res['partner_id'] = emp_record.partner_id.id
                if 'basic_salary' in fields:
                    res['basic_salary'] = emp_record.basic_salary
                if 'from_date' in fields:
                    res['from_date'] = emp_record.from_date
                if 'to_date' in fields:
                    res['to_date'] = emp_record.to_date
                if 'net_salary' in fields:
                    res['net_salary'] = emp_record.net_salary
                if 'gross_salary' in fields:
                    res['gross_salary'] = emp_record.gross_salary
                if 'commision' in fields:
                    res['commision'] = emp_record.commision
                if 'extra_allowances' in fields:
                    res['extra_allowances'] = emp_record.extra_allowances
                
        else:
            raise UserError('No employee record found for the current user.')
        return res
    

    def product_bill(self):
        product = self.env.ref('emp.my_employee_payslip')

        invoices = []

        
        start_date = self.from_date
        end_date = self.to_date
        
        while start_date <= end_date:
            invoices.append({
                'move_type': 'in_invoice',
                'partner_id': self.partner_id.id,
                'invoice_date': start_date,
                'invoice_line_ids': [(0, 0, {
                    'product_id': product.id,
                    'quantity': 1,
                    'price_unit': self.basic_salary,
                })],
            })

            start_date = start_date.replace(day=1) + timedelta(days=32)
            start_date = start_date.replace(day=1)

        # Create the bill
        bill = self.env['account.move'].create(invoices)

        # Post the bill
        bill.action_post()

        journal_id = self.env['account.journal'].search([('type', '=', 'bank')], limit=1)   
        # partner_bank_id = self.env['account.move'].search([('partner_id', '=', self.partner_id.id)], limit=1)
        payments = {
            'payment_type': 'outbound',
            'partner_type': 'supplier',
            'partner_id': self.partner_id.id,
            'amount': self.basic_salary,
            'journal_id': journal_id.id, 
            # 'partner_bank_id': partner_bank_id.id,
            }

        # payment = self.env['account.payment'].create(payments) 
        # payment.action_post()       
        print(payments)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            # 'action': 'action_register_payment',
            'res_id': bill.id,
            # 'domain': [('partner_id', '=', self.partner_id.id)],
        }
