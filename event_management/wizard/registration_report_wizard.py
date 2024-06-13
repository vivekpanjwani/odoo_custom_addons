# coding: utf-8
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64
import csv
import io
from io import StringIO

from odoo import models, fields, api

class RegistrationReport(models.TransientModel):
    _name = 'registration.report.wizard'
    _description = 'Report'

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    generated_csv_file = fields.Binary("Generated Csv")
    file = fields.Binary('Export File')
    filename = fields.Char('File Name')

    def _generate_row(self, event):
        """ Generates a single row in the output CSV. Will attribute the total to the box specified on the partner. """
        event_states = self.env['event.registration'].sudo().search([])
        row = [
            event.registration_date,
            event.event_id.organizer_id.name,
            event.attendee_id.name,
            event.event_id.name,
            event_states._get_state_display(event.state),
        ]
        row = [val or "-" for val in row]
        return row

    def action_generate(self):
        """ Called from UI. Generates the CSV file in memory and writes it to the generated_csv_file
        field. Then returns an action for the client to download it. """
        self.ensure_one()
        header = ["Registration Date","Organizer Name","Attendee Name","Event Name","Registration State"]

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(header)
        event_datas = self.env['event.registration'].sudo().search([
            # ('registration_date', '<=', self.end_date),
            # ('registration_date', '>=', self.start_date),
            ('state','!=', 'cancelled')
            ])
        for line in event_datas:
            new_row = self._generate_row(line)
            writer.writerow(new_row)

        self.generated_csv_file = base64.b64encode(output.getvalue().encode())

        return {
            "type": "ir.actions.act_url",
            "target": "self",
            "url": "/web/content?model=registration.report.wizard&download=true&field=generated_csv_file&filename=Event Registration.csv&id={}".format(
                self.id)}