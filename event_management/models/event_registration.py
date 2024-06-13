# -*- coding: utf-8 -*-

from odoo import models, fields


class EventRegistration(models.Model):
    _name = 'event.registration'
    _description = 'Event Registration'
    _rec_name = "attendee_id"

    attendee_id = fields.Many2one(
        comodel_name="event.attendee",
        required=False
        )
    event_id = fields.Many2one(comodel_name="event.event")
    registration_date = fields.Datetime(string="Registration Date")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ],
        default="draft",
        string="State",
        store=True)

    def _get_state_display(self, state):
        state_mapping = {
            'draft': 'Draft',
            'confirmed': 'Confirmed',
            'cancelled': 'Cancelled',
        }
        return state_mapping.get(state, '-')
        
    # Buttons
    def button_confirm(self):
        """Send mail and make state confirmed"""
        self.state = 'confirmed'
        self.send_email('event_management.email_template_registration')

    def button_cancel(self):
        """Send mail and make state cancelled"""
        self.state = 'cancelled'
        self.send_email('event_management.email_template_cancellation')

    def send_email(self, template_xml_id):
        """Send Mail according to template_xml_id"""
        template = self.env.ref(template_xml_id)
        if template:
            template.send_mail(self.id)

