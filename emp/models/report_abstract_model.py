from odoo import api, models

class AccountMoveReport(models.AbstractModel):
    _name = 'report.emp.report_payslip'
    _description = 'Account Move Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['account.move'].browse(docids)

        emp_model_data = {}
        for move in docs:
            emp_model_obj = self.env['emp.model'].search([('partner_id', '=', move.partner_id.id)], limit=1)
            if emp_model_obj:
                emp_model_data[move.id] = emp_model_obj.read()[0]

        return {
            'doc_ids': docids,
            'doc_model': 'emp.model',
            'docs': docs,
            'emp_model_data': emp_model_data,
        }