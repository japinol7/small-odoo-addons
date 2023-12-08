# -*- coding: utf-8 -*-
from odoo import fields, models


class JapAddonsConfig(models.Model):
    _inherit = 'jap.addons.config'

    prefix_msg_create_invoice_sel_wiz = fields.Char(
        string="Prefix Msg Create Invoice Selected Wizard",
        help="Prefix Message for Create Invoice from Selected Lines Wizard.")

    @staticmethod
    def get_prefix_msg_create_invoice_sel_wiz(recordset):
        return recordset.env['jap.addons.config'].sudo().browse(
            recordset.env.ref('jap_addons_config.jap_addons_config_main').id
            ).prefix_msg_create_invoice_sel_wiz
