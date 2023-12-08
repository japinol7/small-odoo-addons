# -*- coding: utf-8 -*-
import logging

from odoo import models, fields


_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    jap_invoice_note = fields.Text(
        string="Invoice Note", readonly=True, copy=False,
        help="Invoice note internal field. "
             "It will not be added to the printed invoice.")
