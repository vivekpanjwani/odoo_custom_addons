from odoo import api, models
from odoo import fields


class SaleCommission(models.AbstractModel):
    _name = 'report.sale_commission.report_commission'
    _description = 'Sale Commission Report'

    @api.model
    def _get_report_values(self, docids, data=None): 
        docs = self.env['sale.commission.details.wizard'].browse(docids)
        users = self.env['res.users'].search([])
        com_total = 0.0
        from_date = docs.from_date
        to_date = docs.to_date
        report_data = {}
        total_commissions = 0
        for user in users:
            total = 0.0
            orders = self.env['sale.order'].search([
                ('user_id', '=', user.id),
                ('date_order', '>=', from_date),
                ('date_order', '<=', to_date),
                ])
            for order in orders:
                for line in order.order_line:
                    total += line.commission_amount
            total_commissions += total
            if total != 0 and orders != False:
                total = round(total, 2)
                report_data[user.id] = total
            
        # print("&***&^&&*&**T^T*T^ ", report_data)
        new_report_data = {}
        users = self.env['res.users'].search([])
        for user in users:
            user_orders = self.env['sale.order'].search([('user_id', '=', user.id), ('date_order', '>=', from_date), ('date_order', '<=', to_date)])
            print("@(*@(@*@(*@(@*(@*@)))))", user_orders)
            user_report_data = []
            total_commission = 0 
            for order in user_orders:
                commission_percentage = order.commission_percentage
                order_total = sum(line.commission_amount for line in order.order_line)
                commission_amount = (order_total*commission_percentage)/100
                total_commission += commission_amount
                user_report_data.append({
                    'order_id': order.name,
                    'order_total': order_total,
                    'commission_percentage': commission_percentage,
                    'commission_amount': commission_amount,
                })
            new_report_data[user.name] = {
                'data': user_report_data,
                'total_commission': total_commission,
            }
            print("*************", new_report_data)


        return {
            'docs': docs,
            'users': users,
            'doc_ids': docids,
            'doc_model': 'sale.commission.details.wizard',
            'report_data': report_data,
            'total_commissions': total_commissions,
            'new_report_data': new_report_data,
            'user_report_data': user_report_data,

        }

    