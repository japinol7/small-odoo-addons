# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError

MAX_BATCH_SIZE = 20


class JapAddonsConfig(models.Model):
    _inherit = 'jap.addons.config'

    bulk_server_job_batch_size = fields.Integer(
        'Bulk server job batch size', default=MAX_BATCH_SIZE,
        required=True, copy=False,
        help="Bulk server job batch size "
             "in the jap.bulk.server.job.job model")
    bulk_job_target_recordset_model = fields.Char(
        string='Target Recordset model', required=True)
    bulk_job_target_domain = fields.Char(
        string='Target domain', required=True)
    bulk_job_target_process_items_func = fields.Char(
        string='Target callable to process items', required=True)

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
