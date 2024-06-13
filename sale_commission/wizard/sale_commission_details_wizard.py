# coding: utf-8
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64
import csv
import io
from io import StringIO
from datetime import date, datetime
from collections import defaultdict
import xlsxwriter
from io import BytesIO

from odoo import fields, models

class SaleCommissionDetailsWizard(models.TransientModel):
	_name = 'sale.commission.details.wizard'
	_description = 'Sale Commission Details Wizard'

	from_date = fields.Date(string="From Date", required=True)
	to_date = fields.Date(string="To date")
	reportby = fields.Selection([
		('by_salesperson', 'Salesperson Commission Summary'),
		 ('by_order', 'Order Commission Summary'),
		 ], string="Report By")

	file = fields.Binary('Export File')
	filename = fields.Char('File Name')


	def action_generate_xlsv(self):
		if self.reportby == 'by_salesperson':
			filename = 'Salesperson Commission Report as on '+str(self.from_date)+ str(self.to_date)
			output = BytesIO()
			workbook = xlsxwriter.Workbook(output, {'in_memory': True})
			worksheet = workbook.add_worksheet()
			headers = ["SalePerson", "Total Commission"]
			header_format = workbook.add_format({'align': 'left', 'bg_color': '#FFDA33'})

			max_lengths = [len(header) for header in headers]

			for col_num, header in enumerate(headers):
				worksheet.write(0, col_num, header, header_format)

			users = self.env['res.users'].search([])
			payments = self.env['account.payment'].sudo().search([("date", "<=", self.to_date),("date", ">=", self.from_date),('partner_type','=','supplier'),('payment_type','=', 'outbound')])
			partners = payments.mapped('partner_id')
			total_commissions = 0
			row_num=0
			for row_num, partner in enumerate(partners, start=1):
				print("PPPPPPPPPPPPPPPPPPPPPPPP", partners)
				partner_amount = self.env['account.payment'].search([('partner_id','=', partner.id),('partner_type','=','supplier'),('payment_type','=', 'outbound')])
				partner_total = sum(partner_amount.mapped('amount'))
				total_commissions += partner_total
				round(total_commissions, 2)

				worksheet.write(row_num,0, partner.name)
				worksheet.write(row_num,1, partner_total)
				max_lengths[0] = max(max_lengths[0], len(partner.name))
				max_lengths[1] = max(max_lengths[1], len(str(partner_total)))
			
			worksheet.write(row_num+1, 0 , "Total Commission")
			worksheet.write(row_num+1, 1 , total_commissions)
			max_lengths[1] = max(max_lengths[1], len(str(total_commissions)))
			for i, width in enumerate(max_lengths):
					worksheet.set_column(i, i, width + 1)


		elif self.reportby == 'by_order':
			filename = 'Order Commission Report as on '+str(self.from_date)+ str(self.to_date)
			output = BytesIO()
			workbook = xlsxwriter.Workbook(output, {'in_memory': True})
			worksheet = workbook.add_worksheet()
			headers = ["Sale Order", "Commission %","Order Total","Order Commission"]
			user_report_data = [] 
			header_format = workbook.add_format({'align': 'left', 'bg_color': '#FFDA33'})

			max_lengths = [len(header) for header in headers]

			for col_num, header in enumerate(headers):
				worksheet.write(0, col_num, header, header_format)

			row_num = 1
			user_format = workbook.add_format({'align': 'left', 'bg_color': '#37B836'})
			total_com_format = workbook.add_format({'align': 'right', 'bg_color': '#37B836'})
			users = self.env['res.users'].search([])
			for user in users:
				user_row = row_num
				worksheet.write(user_row, 0, user.name, user_format)
				max_lengths[0] = max(max_lengths[0], len(user.name))

				row_num += 1
				user_orders = self.env['sale.order'].search([('user_id', '=', user.id), ("date_order", "<=", self.to_date),("date_order", ">=", self.from_date)])
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
						'total_commission': total_commission,
					})
					print("%$#$#$#$#%#$#$#", user_report_data)
					worksheet.write(row_num, 0, order.name)
					worksheet.write(row_num, 1, commission_percentage)
					worksheet.write(row_num, 2, order_total)
					worksheet.write(row_num, 3, commission_amount)
					max_lengths[0] = max(max_lengths[0], len(order.name))
					max_lengths[1] = max(max_lengths[1], len(str(commission_percentage)))
					max_lengths[2] = max(max_lengths[2], len(str(order_total)))
					max_lengths[3] = max(max_lengths[3], len(str(commission_amount)))
					row_num += 1
				worksheet.write(user_row, 3, total_commission, total_com_format)
				max_lengths[3] = max(max_lengths[3], len(str(total_commission)))

			for i, width in enumerate(max_lengths):
				worksheet.set_column(i, i, width + 1)
		workbook.close()    
		output.seek(0)
		xlsx_content = output.getvalue()

		# Update the file name
		file_name = filename +'.xlsx'

		# Encode content to base64
		xlsx_base64 = base64.b64encode(xlsx_content)

		self.write({
			'file': xlsx_base64,
			'filename': filename,
		})
		return {
			'type': 'ir.actions.act_url',
			'url': "web/content/?model=sale.commission.details.wizard&id=" + str(self.id) + "&filename_field=filename&field=file&download=true&filename="+file_name,
			'target': 'self'
		}