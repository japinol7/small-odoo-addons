# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.safe_eval import safe_eval

_logger = logging.getLogger(__name__)

MAX_BATCH_SIZE = 20
MAX_ITEMS_TO_PROCESS = 6000


class JapSimpleBulkServerJob(models.Model):
    _name = "jap.simple.bulk.server.job"
    _description = "JAP Simple Bulk Server Job"
    _order = "id desc"

    state = fields.Selection([
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
        ('failed', 'Failed'),
        ],
        default='pending')
    max_items_to_process = fields.Integer(
        required=True, copy=False)
    processed_items_count = fields.Integer(
        default=0, copy=False)
    last_item_id = fields.Integer(
        string='Last item Id', default=0, copy=False)
    error_message = fields.Text(
        copy=False)
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
    active = fields.Boolean(default=True)

    @api.constrains('max_items_to_process')
    def _check_max_items_to_process(self):
        for job in self:
            if not 1 <= job.max_items_to_process <= MAX_ITEMS_TO_PROCESS:
                raise ValidationError(_(
                    "The number of items to process must be between 1 and %s."
                    ) % MAX_ITEMS_TO_PROCESS)

    def copy(self, default=None):
        raise UserError('Not allowed: copy a JAP Simple Bulk Server Job.')

    def action_cancel(self):
        if self.filtered(
                lambda job: job.state in ('done', 'cancel', 'failed')):
            raise UserError("User Error: Cannot cancel jobs in the following "
                            "states: 'done', 'cancel', 'failed'.")

        return self.write({'state': 'cancel'})

    def action_running(self):
        if self.filtered(
                lambda job: job.state in ('done', 'pending', 'running')):
            raise UserError(
                "User Error: Cannot set jobs state to 'running' if they are in "
                "the following states: 'done', 'pending', 'running'.")

        return self.write({'state': 'running'})

    def _process_job_batch_items(self, items):
        """Processes a batch and update its progress checkpoint.
        Transaction management is handled by _run_items_processing().
        """
        self.ensure_one()

        process_items_func = getattr(
            items, self.target_process_items_func, None)

        if not callable(process_items_func):
            raise ValidationError(
                _("Method '%s' not found or not callable on model '%s'.")
                % (self.target_process_items_func, self.target_recordset_model))

        # Execute the configured recordset method
        process_items_func()

        # Update progress only after successful business processing
        self.processed_items_count += len(items)
        self.last_item_id = items[-1].id

        if self.processed_items_count >= self.max_items_to_process:
            self.state = 'done'

    def _get_domain_for_items_to_process(self):
        error_msg = ''
        try:
            domain = [('id', '>', self.last_item_id)]
            domain.extend(safe_eval(self.target_domain))
        except Exception as e:
            _logger.exception(
                "Error getting the domain for the items to process")
            domain = None
            error_msg = str(e)

        return domain, error_msg

    def _run_items_processing(self):
        """Runs one batch. Is intended to be executed by a cron."""
        self.ensure_one()

        if self.state in ('done', 'failed'):
            return

        if not self.target_domain:
            self.state = 'done'
            return

        domain, error_msg = self._get_domain_for_items_to_process()

        if error_msg:
            self.state = 'failed'
            self.error_message = _(
                "Error getting the domain for items to process.\n%s"
                ) % error_msg
            return

        remaining = self.max_items_to_process - self.processed_items_count

        if remaining <= 0:
            self.state = 'done'
            return

        try:
            batch_size = self.env[
                'jap.addons.config'
                ].get_bulk_server_job_batch_size(self)

            batch_size = min(batch_size, MAX_BATCH_SIZE)

            if batch_size <= 0:
                raise ValidationError(
                    _("The configured batch size must be greater than zero."))

            items = self.env[self.target_recordset_model].search(
                domain,
                limit=min(batch_size, remaining),
                order='id')

            if not items:
                self.state = 'done'
                return

            _logger.info(
                "Processing item batch (max %s) first_id -> last_id: %s -> %s",
                batch_size,
                items[0].id, items[-1].id)

            # The batch is atomic: on failure, all database changes
            # made since entering this savepoint are rolled back.
            with self.env.cr.savepoint():
                self.state = 'running'
                self._process_job_batch_items(items)

        except Exception as e:
            _logger.exception("Error processing bulk job batch")

            # The savepoint has rolled back the failed batch.
            # Record the failure outside the savepoint so it can
            # be committed by Odoo with the outer cron transaction.
            self.state = 'failed'
            self.error_message = _("Error processing items.\n%s") % str(e)

    @api.model
    def _get_current_items_bulk_processing_job(self):
        """Returns at most one active job for each cron execution.
        Adjusts the cron frequency and batch size to balance processing
        throughput against resource usage.
        """
        return self.search([
            ('state', 'in', ['pending', 'running']),
            ('active', '=', True),
            ], limit=1, order='id')

    @api.model
    def _cron_process_items_bulk_processing_job(self):
        job = self._get_current_items_bulk_processing_job()

        if not job:
            return

        job._run_items_processing()

    def action_jap_simple_bulk_server_job(self):
        res = self.env['ir.actions.act_window']._for_xml_id(
            'jap_simple_bulk_server_job.action_jap_simple_bulk_server_job_wizard')
        return res
