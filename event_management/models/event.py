# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Event(models.Model):
    _name = 'event.event'
    _description = 'Event Management'

    # General Fields
    name = fields.Char(string="Event Name", required=True)
    description = fields.Text(string="Description")
    start_date = fields.Datetime(string="Start Date")
    end_date = fields.Datetime(string="End Date")
    color = fields.Integer('color', default=1)

    # ----Many2one Field ----
    organizer_id = fields.Many2one(
        comodel_name='event.organizer',
        string="Event Organizer")

    # ----Many2many Field ----
    attendee_ids = fields.Many2many(
        comodel_name='event.attendee',
        relation='event_registration',
        column1='event_id',
        column2='attendee_id',
        compute='_compute_confirmed_attendees',
        readonly=True
        ) 
    duration = fields.Float(string="Duration", compute="_compute_duration")
    attendee_count = fields.Integer(string="Attendee Count",
        compute='_compute_attendee_count')

    registration_ids = fields.One2many('event.registration', 'event_id')

    # Compute Method
    @api.depends('start_date', 'end_date')
    def _compute_duration(self):
        """
        Calculate the duration from start_date to end_date
        """
        for record in self:
            if record.start_date and record.end_date:
                start_date = fields.Datetime.from_string(record.start_date)
                end_date = fields.Datetime.from_string(record.end_date)
                duration = end_date - start_date
                record.duration = duration.days + 1
            else:
                record.duration = 0.0


    @api.depends('attendee_ids')
    def _compute_attendee_count(self):
        """
        Counts the attendees
        """
        for record in self:
            record.attendee_count = len(record.attendee_ids)

    @api.depends('registration_ids.state')
    def _compute_confirmed_attendees(self):
        """
        Compute attendees_ids according to confirmed states from registration_ids
        """
        for record in self:
            record.attendee_ids = record.registration_ids.filtered(lambda r: r.state == 'confirmed').mapped('attendee_id')
            