# -*- coding: utf-8 -*-
import logging

from odoo import models
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def action_jap_copy_sale_order_line(self):
        self.ensure_one()

        if not self.env.user.has_group('jap_custom_security.group_sale_copy_lines'):
            raise ValidationError(
                f"You are not allowed to duplicate order lines.\n\n"
                f"{self.env['jap.addons.config'].get_warning_msg_security_restriction(self)}")
        super().action_jap_copy_sale_order_line()
