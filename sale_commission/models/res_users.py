from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    commission_percentage = fields.Float(string="Commission Percentage")

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_commission_paid = fields.Boolean(string="Is Commission Paid", default=False)

    all_invoices_paid = fields.Boolean(compute='_compute_all_invoices_paid', store=True)
    commission_percentage = fields.Float(string="Commission Percentage", compute="_compute_commission_percentage", store=True)
    
    @api.depends('invoice_ids.payment_state')
    def _compute_all_invoices_paid(self):
        for order in self:
            temp = False
            for invoice in order.invoice_ids:
                if invoice.payment_state in ['paid', 'in_payment']:
                    temp = True
                else:
                    temp = False
                    break
            order.all_invoices_paid = temp


    @api.depends('user_id')
    def _compute_commission_percentage(self):
        for order in self:
            if order.is_commission_paid == False:
                order.commission_percentage = order.user_id.commission_percentage
                
    def pay_commission(self):
        self.ensure_one()
        partner_id = self.user_id.partner_id.id
        journal_id = self.env['account.journal'].search([('type', '=', 'bank')], limit=1)  
        commission_amount = sum(line.commission_amount for line in self.order_line)
        bill = self.env['account.payment'].create({
            'payment_type': 'outbound',
            'partner_type': 'supplier',
            'partner_id': partner_id,
            'amount': commission_amount,
            'journal_id': journal_id.id,
            'ref': 'commission_payment',
            'so_id': self.id,
        })
        bill.action_post()
        self.is_commission_paid = True

    def payment_check(self):
        self.ensure_one()
        payment_id = self.env['account.payment'].search([('so_id', '=', self.id)])
        action = self.env.ref('account.action_account_payments_payable').read()[0]
        form_view = self.env.ref('account.view_account_payment_form').id
        action['views'] = [(form_view, 'form')]
        action['res_id'] = payment_id.id
        return action

