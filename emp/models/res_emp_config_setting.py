# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    probation_period_in_days = fields.Integer("Probation Period")
    notice_period_in_days = fields.Integer("Notice Period")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            probation_period_in_days=self.env['ir.config_parameter'].sudo().get_param('probation_period_in_days'),
            notice_period_in_days=self.env['ir.config_parameter'].sudo().get_param('notice_period_in_days'),
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('probation_period_in_days', self.probation_period_in_days)
        self.env['ir.config_parameter'].sudo().set_param('notice_period_in_days', self.notice_period_in_days)