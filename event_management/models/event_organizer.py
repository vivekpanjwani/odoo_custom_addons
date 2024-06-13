# -*- coding: utf-8 -*-

from odoo import models,fields,api


class EventOrganizer(models.Model):
    _name = 'event.organizer'
    _description = 'Event Organizer'

    name = fields.Char(string="Organizer Name", required=True)
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    user_id = fields.Many2one(comodel_name="res.users",readonly=True)
    event_ids = fields.One2many('event.event', 'organizer_id')
    color = fields.Integer('color', default=1)

    # Create Methods
    @api.model_create_multi
    def create(self, vals_list):
        """
        Creates new user on creating new record 
        """
        for vals in vals_list:
            existing_record = self.search([('name', '=', vals.get('name'))],
                limit=1)
            if existing_record:
                # Create a duplicate record
                vals['name'] = "{} (copy)".format(vals['name'])
                duplicate_record = self.create(vals)
                return duplicate_record
            
            user_vals = {
                'name': vals.get('name'),
                'login': vals.get('email'),
            }
            user_id = self.env['res.users'].create(user_vals)
            vals['user_id'] = user_id.id
   
        return super().create(vals_list)
