# -*- coding: utf-8 -*-
import logging

from odoo import fields, models
from odoo.exceptions import UserError


_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    jap_created_by_copy = fields.Boolean(
        string="Has been created by duplication",
        readonly=True, copy=False,
        help="Whether has been created by duplication")

    def action_jap_copy_sale_order_line(self):
        self.ensure_one()

        if self.order_id.state == 'cancel':
            raise UserError('Cannot duplicate an order line from a canceled order.')
        if self.order_id.invoice_status == 'invoiced':
            raise UserError('Cannot duplicate order lines from a fully invoiced order.')

        new_order_line = self.copy({
            'jap_created_by_copy': True,
            'order_id': self.order_id.id,
            'product_uom_qty': 0,
            'price_unit': 0,
            })

        _logger.info(f"Jap. Created sale line. Id: {new_order_line.id}. "
                     f"Copied from line id: {self.id}. User: {self.env.user.id}")
        self.order_id.message_post(
            body=f"Duplicated sale line with product: {self.product_id.display_name}")

    def action_jap_do_nothing(self):
        pass
