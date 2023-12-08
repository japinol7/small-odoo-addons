# -*- coding: utf-8 -*-
from odoo import fields, models


class JapAddonsConfig(models.Model):
    _inherit = 'jap.addons.config'

    warning_msg_security_restriction = fields.Char(
        string="Warning msg security restriction")

    @staticmethod
    def get_warning_msg_security_restriction(recordset):
        return recordset.env['jap.addons.config'].sudo().browse(
            recordset.env.ref('jap_addons_config.jap_addons_config_main').id
            ).warning_msg_security_restriction
