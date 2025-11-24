# -*- coding: utf-8 -*-
import logging
from time import sleep

from odoo import api, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _create_invoices(self, grouped=False, final=False, date=None):
        """Override to set invoice lines as copied if the original sale line
        was copied with our custom feature.
        """
        invoices = super()._create_invoices(grouped=grouped, final=final, date=date)

        if invoices:
            self._jap_set_invoice_lines_created_from_copied_sale_lines(invoices)

        return invoices

    def _jap_set_invoice_lines_created_from_copied_sale_lines(self, invoices):
        for move_line in invoices.invoice_line_ids:
            if any(move_line.sale_line_ids.filtered(
                    lambda line: line.jap_created_by_copy)):
                move_line.jap_sale_line_created_by_copy = True

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

    def action_jap_sale_orders_same_partner(self):
        self.ensure_one()
        return self.env['jap.sale.orders.same.partner.wizard']. \
            create({
                'partner_id': self.partner_id.id,
            }).action_open()

    @api.model
    def jap_waste_some_time(self, time_to_waste: int) -> int:
        """Waste some time by sleeping time_to_waste seconds.
        Returns how many seconds we effectively wasted.
        Currently, we set a max time to waste in the method body.
        It is intended to be used to test remote JSON-RPC calls behavior.
        """
        log_prefix = f"{'-' * 10} "
        _logger.info(f"{log_prefix}Start jap_waste_some_time")

        max_time_to_waste = 30
        if time_to_waste > max_time_to_waste:
            _logger.info(f"{log_prefix}Too much time to waste: {time_to_waste}. "
                         f"We will waste {max_time_to_waste} secs, instead.")
            time_to_waste = max_time_to_waste

        for i in range(1, time_to_waste + 1):
            _logger.info(f"{log_prefix}Wasting your time: {i:2} / {time_to_waste:2}")
            sleep(1)

        _logger.info(f"{log_prefix}End jap_waste_some_time")

        return time_to_waste
