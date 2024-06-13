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

from odoo import models, fields, api

class EmpDataExport(models.TransientModel):
    _name = 'emp.data.export'
    _description = 'Employee Data'

    partner_id = fields.Many2one('res.partner')
    before_date = fields.Date(string="Before Date", required=True)
    generated_csv_file = fields.Binary("Generated Csv")
    file = fields.Binary('Export File')
    filename = fields.Char('File Name')

    def _generate_row(self, employee):
        """ Generates a single row in the output CSV. Will attribute the total to the box specified on the partner. """
        row = [
            employee.dob,
            employee.name,
            employee.basic_salary,
            employee.age,
            employee.email,
            employee.phone,
            employee.street,
            employee.street2,
            employee.city.name if employee.city else "-",
            employee.state_id.name if employee.state_id else "-",
            employee.country_id.name if employee.country_id else "-",
        ]
        row = [val or "-" for val in row]
        return row

    def action_generate(self):
        """ Called from UI. Generates the CSV file in memory and writes it to the generated_csv_file
        field. Then returns an action for the client to download it. """
        self.ensure_one()
        header = ["DOB","Name","Basic Salary","Age","Email","Phone","Street1","Street2","City","State","Country",]

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(header)
        emp_datas = self.env['emp.model'].sudo().search([
            ("dob", "<=", self.before_date),
            ])
        
        for line in emp_datas:
            new_row = self._generate_row(line)
            writer.writerow(new_row)

        # for read_group
        domain = [("joining_date", "<=", fields.Date.today())]
        fields_to_read = ['name', 'joining_date', 'released_date', 'states']
        group_by = ['states']

        emp_data_read = self.env['emp.model'].sudo().read_group(domain, fields_to_read, group_by)

        for line in emp_data_read:
            print(line)
        # ----------------------

        self.generated_csv_file = base64.b64encode(output.getvalue().encode())

        return {
            "type": "ir.actions.act_url",
            "target": "self",
            "url": "/web/content?model=emp.data.export&download=true&field=generated_csv_file&filename=EmployeeData.csv&id={}".format(
                self.id)}


    def action_generate_xlsv(self):
        filename = 'Employee Report as on '+str(self.before_date)
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})

        emp_datas = self.env['emp.model'].sudo().search([("dob", "<=", self.before_date)])

        for index, emp_data in enumerate(emp_datas):
            worksheet = workbook.add_worksheet('Sheet{}'.format(index + 1))
            headers = ["DOB","Name","Basic Salary","Age","Email","Phone","Street1","Street2","City","State","Country",]
            data = [
                str(emp_data.dob),
                emp_data.name,
                emp_data.basic_salary,
                emp_data.age,
                emp_data.email,
                emp_data.phone,
                emp_data.street,
                emp_data.street2,
                emp_data.city.name if emp_data.city else "-",
                emp_data.state_id.name if emp_data.state_id else "-",
                emp_data.country_id.name if emp_data.country_id else "-",
            ]            
            data = [val or "-" for val in data]

            for col_num, (header, cell_data) in enumerate(zip(headers, data)):
                worksheet.write(0, col_num, header)
                worksheet.write(1, col_num, str(cell_data))

        workbook.close()
        output.seek(0)
        xlsx_content = output.getvalue()
        
        # Update the file name
        file_name = filename +'.xlsx'

        # Encode content to base64
        xlsx_base64 = base64.b64encode(xlsx_content)
        '''
        self.write({
            'file': csv_base64,
            'filename': file_name,
        })
        '''
        self.write({
             'file': xlsx_base64,
            'filename': filename,
        })
        return {
            'type': 'ir.actions.act_url',
            'url': "web/content/?model=emp.data.export&id=" + str(self.id) + "&filename_field=filename&field=file&download=true&filename="+file_name,
            'target': 'self'
        }

        def action_generate(self):
                """ Called from UI. Generates the CSV file in memory and writes it to the generated_csv_file
                field. Then returns an action for the client to download it. """
                self.ensure_one()
                header = ["DOB","Name","Basic Salary","Age","Email","Phone","Street1","Street2","City","State","Country",]

                output = io.StringIO()
                writer = csv.writer(output)
                writer.writerow(header)
                domain = [("joining_date", "<=", fields.Date.today())]
                fields_to_read = ['name', 'joining_date', 'released_date', 'states']
                group_by = ['states']

                emp_datas = self.env['emp.model'].sudo().read_group(domain, fields_to_read, group_by)

                for line in emp_datas:
                    print(line)