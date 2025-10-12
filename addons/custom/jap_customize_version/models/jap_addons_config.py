# -*- coding: utf-8 -*-
from odoo import fields, models


class JapAddonsConfig(models.Model):
    _inherit = 'jap.addons.config'

    jap_custom_version = fields.Char(
        'Jap custom version',
        compute='_compute_jap_custom_version')

    def _compute_jap_custom_version(self):
        version = self.env['jap.customize.version'].get_jap_custom_version()
        for rec in self:
            rec.jap_custom_version = version
