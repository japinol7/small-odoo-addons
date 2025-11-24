# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class JapCreateInvoiceSelectedSaleLinesWizard(models.TransientModel):
    """This wizard allows creating invoices from only the selected sale lines."""

    _name = "jap.create.invoice.selected.sale.lines.wizard"
    _description = "This wizard allows creating invoices from only the selected sale lines."

    def _default_sale_id(self):
        context = self.env.context
        if context.get('active_model') != 'sale.order':
            raise ValidationError('Wrong Active_model. Should be sale.order!')

        active_id = context.get('active_id')
        if active_id:
            return self.env['sale.order'].browse(active_id)[0]

    def _prepare_line_all_domain(self):
        return [
            ('order_id', '=', self._default_sale_id().id),
            ('invoice_status', '=', 'to invoice'),
            ('qty_to_invoice', '>', 0),
            ]

    def _default_line_all_ids(self):
        return (self.env['sale.order.line'].
                search(self._prepare_line_all_domain()))

    def _prepare_line_sel_domain(self):
        domain = self._prepare_line_all_domain()
        domain.append(('name', '=', 'Nothing'))
        return domain

    def _prepare_line_not_sel_domain(self):
        return self._prepare_line_all_domain()

    def _default_line_sel_ids(self):
        domain = self._prepare_line_sel_domain()
        return self.env['sale.order.line'].search(domain)

    def _default_line_not_sel_ids(self):
        domain = self._prepare_line_not_sel_domain()
        return self.env['sale.order.line'].search(domain)

    sale_id = fields.Many2one(
        'sale.order',
        string='Sale', readonly=True,
        default=_default_sale_id)
    sale_name = fields.Char(
        string='Sale', readonly=True)
    partner_id = fields.Many2one(
        'res.partner',
        string='Customer', readonly=True)
    date_order = fields.Date(
        string='Date order', readonly=True,
        help="Date on which the sales order was created.")
    invoice_note = fields.Text(
        help="Add note to the created invoice. "
             "It will not be added to the printed invoice.")
    line_ids_all_ids = fields.Many2many(
        'sale.order.line',
        relation='sale_line_invoice_all_sale_lines_wiz_rel',
        string='All Sale Order Lines',
        default=_default_line_all_ids)
    line_ids_sel_ids = fields.Many2many(
        'sale.order.line',
        relation='sale_line_invoice_sel_sale_lines_wiz_rel',
        string='Selected Lines to Invoice',
        default=_default_line_sel_ids)
    line_ids_not_sel_ids = fields.Many2many(
        'sale.order.line',
        relation='sale_line_invoice_no_sel_sale_lines_wiz_rel',
        string='Not Selected Lines to Invoice',
        default=_default_line_not_sel_ids)

    @api.onchange('sale_id')
    def _onchange_sale_id(self):
        return {
            'domain': {
                'line_ids_all_ids': self._prepare_line_all_domain(),
                'line_ids_sel_ids': self._prepare_line_sel_domain(),
                'line_ids_not_sel_ids': self._prepare_line_not_sel_domain(),
                }
            }

    @api.onchange('line_ids_sel_ids')
    def _onchange_line_ids_sel_ids(self):
        lines = self.line_ids_all_ids - self.line_ids_sel_ids
        self.update({'line_ids_not_sel_ids': lines.ids})

    @api.onchange('line_ids_not_sel_ids')
    def _onchange_line_ids_not_sel_ids(self):
        lines = self.line_ids_all_ids - self.line_ids_not_sel_ids
        self.update({'line_ids_sel_ids': lines.ids})

    def _action_do_not_close(self):
        """Allows keeping the wizard open after executing an action."""
        return {
            'name': _('Invoice Selected Sale Lines'),
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
            'context': self.env.context,
            }

    def set_all_lines_to_invoice(self):
        self.update({
            'line_ids_sel_ids': self.line_ids_all_ids,
            'line_ids_not_sel_ids': self.env['sale.order.line'],
            })
        return self._action_do_not_close()

    def set_all_lines_to_not_invoice(self):
        self.update({
            'line_ids_sel_ids': self.env['sale.order.line'],
            'line_ids_not_sel_ids': self.line_ids_all_ids,
            })
        return self._action_do_not_close()

    def set_invoice_note(self, move_ids):
        for move in self.env['account.move'].search([('id', 'in', move_ids)]):
            move.jap_invoice_note = self.invoice_note

    def add_message_to_created_invoice(self, move_ids, sale_order, body_msg):
        for move in self.env['account.move'].search([('id', 'in', move_ids)]):
            move.message_post(body=f"{body_msg}. From Sale: {sale_order.name}")

    def create_invoice(self):
        self.ensure_one()
        msg_prefix = self.env[
            'jap.addons.config'].get_prefix_msg_create_invoice_sel_wiz(self)
        msg_create_invoice = "Create Invoice from Selected Sale Lines."

        lines = self.line_ids_sel_ids
        if not lines:
            raise UserError(
                "There is no order line selected to create an invoice!")

        self = self.with_context(
            jap_sale_lines_selected_to_create_invoice=[x.id for x in lines])
        sale_order = self.sale_id

        _logger.info(f"{msg_prefix} Create invoice for order lines: "
                     f"{[(line.id, line.order_id.name) for line in lines]}")
        moves = sale_order._create_invoices(grouped=False, final=False)
        move_ids = [move.id for move in moves]

        self.set_invoice_note(move_ids)
        self.add_message_to_created_invoice(
            move_ids, sale_order, body_msg=msg_create_invoice)

        sale_order.message_post(body=msg_create_invoice)
        return {'type': 'ir.actions.client', 'tag': 'soft_reload'}
