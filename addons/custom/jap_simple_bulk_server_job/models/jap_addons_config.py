# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError

BATCH_SIZE_DEFAULT = 10
MAX_BATCH_SIZE = 20


class JapAddonsConfig(models.Model):
    _inherit = 'jap.addons.config'

    bulk_server_job_batch_size = fields.Integer(
        'Bulk server job batch size', default=BATCH_SIZE_DEFAULT,
        required=True, copy=False,
        help="Bulk server job batch size to use "
             "in the jap.simple.bulk.server.job model")
    bulk_job_target_recordset_model = fields.Char(
        string='Target Recordset model')
    bulk_job_target_domain = fields.Char(
        string='Target domain')
    bulk_job_target_context = fields.Char(
        string='Target context to add to the target recordset',
        help="Target context to add to the target recordset")
    bulk_job_target_process_items_func = fields.Char(
        string='Target callable to process items')
    bulk_job_target_process_func_args = fields.Char(
        string='Target args for the callable func',
        help="Positional arguments to pass to the target function method.")
    bulk_job_target_process_func_kwargs = fields.Char(
        string='Target kwargs for the callable func',
        help="Keyword arguments to pass to the target function method.")

    @api.onchange('bulk_server_job_batch_size')
    def _onchange_bulk_server_job_batch_size(self):
        if not self.bulk_server_job_batch_size \
                or self.bulk_server_job_batch_size < 1:
            raise UserError(
                "You cannot set the bulk server job batch size "
                "to less than 1 item.")

        if self.bulk_server_job_batch_size > MAX_BATCH_SIZE:
            raise UserError(
                "You cannot set the bulk server job batch size "
                "to more than %s items at once."
                % MAX_BATCH_SIZE)

    @staticmethod
    def get_bulk_server_job_batch_size(recordset):
        return recordset.env['jap.addons.config'].sudo().browse(
            recordset.env.ref('jap_addons_config.jap_addons_config_main').id
            ).bulk_server_job_batch_size
