# -*- coding: utf-8 -*-
import logging

from odoo import models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _get_invoiceable_lines(self, final=False):
        """Only allows invoicing the selected lines if this feature
        is activated in the context.
        """
        invoiceable_lines = super()._get_invoiceable_lines(final)

        if 'jap_sale_lines_selected_to_create_invoice' in self.env.context:
            lines_to_invoice = self.env.context.get(
                'jap_sale_lines_selected_to_create_invoice', [])
            return invoiceable_lines.filtered(
                lambda line: line.id in lines_to_invoice)

        return invoiceable_lines

    def action_jap_create_invoice_from_selected_lines(self):
        self.ensure_one()
        if self.state != 'sale':
            raise UserError(
                "Cannot create an invoice from this sale. "
                "It must be in the Sale Order status.")

        res = self.env['ir.actions.act_window']._for_xml_id(
            'jap_sale.action_jap_create_invoice_selected_sale_lines_wizard')

        res['context'] = safe_eval(res['context'])
        res['context'].update({
            'default_sale_name': self.name,
            'default_sale_id': self.id,
            'default_partner_id': self.partner_id.id,
            'default_date_order': self.date_order,
            })
        return res
