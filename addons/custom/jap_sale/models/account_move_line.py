# -*- coding: utf-8 -*-
import logging

from odoo import fields, models


_logger = logging.getLogger(__name__)


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    jap_sale_line_created_by_copy = fields.Boolean(
        string="Related sale line has been created by duplication",
        readonly=True, copy=False,
        help="Whether any related sale line has been created by duplication")

    def action_jap_do_nothing(self):
        pass
