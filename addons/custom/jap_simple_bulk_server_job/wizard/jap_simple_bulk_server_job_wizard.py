# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError

MAX_ITEMS_TO_PROCESS = 6000


class JapSimpleBulkServerJobWizard(models.TransientModel):
    """This wizard allows creating a job to process several records in bulk."""

    _name = "jap.simple.bulk.server.job.wizard"
    _description = "Create a job to process several records in bulk"

    max_items_to_process = fields.Integer(
        string="Max. items to process",
        required=True,
        default=1)
    target_recordset_model = fields.Char(
        string='Target Recordset model', required=True)
    target_domain = fields.Char(
        string='Target domain', required=True)
    target_process_items_func = fields.Char(
        string='Target callable to process items', required=True,
        help="The target callable must be a regular recordset method. "
             "If you need to call an @api.model method, you can wrap it "
             "in a regular recordset method. "
             "Warning: retrying a failed job by setting its state back "
             "to 'running' relies on the target method not manually "
             "committing database changes. Manual commits can prevent "
             "the failed batch from being fully rolled back.")

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        # Load target fields from jap addons config
        config_env = self.env.ref('jap_addons_config.jap_addons_config_main')
        res['target_recordset_model'] = config_env.bulk_job_target_recordset_model
        res['target_domain'] = config_env.bulk_job_target_domain
        res['target_process_items_func'] = config_env.bulk_job_target_process_items_func

        return res

    @api.onchange('max_items_to_process')
    def _onchange_max_items_to_process(self):
        if not self.max_items_to_process or self.max_items_to_process < 1:
            raise UserError(
                "You cannot process less than 1 item.")

        if self.max_items_to_process > MAX_ITEMS_TO_PROCESS:
            raise UserError(
                "You cannot process more than %s items at once."
                % MAX_ITEMS_TO_PROCESS)

    def _save_target_fields(self):
        config_env = self.env.ref('jap_addons_config.jap_addons_config_main')
        config_env.bulk_job_target_recordset_model = self.target_recordset_model
        config_env.bulk_job_target_domain = self.target_domain
        config_env.bulk_job_target_process_items_func = self.target_process_items_func

    def process_items_bulk(self):
        self.ensure_one()

        self._save_target_fields()

        if self.env['jap.simple.bulk.server.job'] \
                ._get_current_items_bulk_processing_job():
            raise UserError(
                "Cannot create a new bulk process job "
                "because another job is already active.")

        job = self.env['jap.simple.bulk.server.job'].create({
            'max_items_to_process': self.max_items_to_process,
            'target_recordset_model': self.target_recordset_model,
            'target_domain': self.target_domain,
            'target_process_items_func': self.target_process_items_func,
            })
        cron = self.env.ref(
            'jap_simple_bulk_server_job.ir_cron_jap_simple_bulk_server_job')

        # Trigger first execution of the cron ASAP
        cron._trigger()

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Started: Job to Process Several Records in Bulk"),
                "message": _(
                    "Job %s to Process Several Records in Bulk has started."
                    ) % job.id,
                "sticky": False,
                "type": "success",
                "next": {
                    "type": "ir.actions.act_window_close",
                    },
                },
            }
