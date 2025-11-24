# -*- coding: utf-8 -*-
from odoo import models, fields, _

import logging

_logger = logging.getLogger(__name__)


class JapSaleOrdersSamePartnerWizard(models.TransientModel):
    _name = "jap.sale.orders.same.partner.wizard"
    _description = "Sale orders with the same customer"

    partner_id = fields.Many2one(
        'res.partner', string="Customer", 
        readonly=True, required=True)
    line_ids = fields.One2many(
        'jap.sale.orders.same.partner.wizard.line',
        inverse_name='wizard_id',
        string="Matches", readonly=True)

    def _fill_lines(self):
        self.ensure_one()
        self.line_ids.unlink()

        if not self.partner_id:
            return

        orders = self.env['sale.order'].sudo().search([
            ('partner_id', '=', self.partner_id.id),
            ], order='id desc')

        lines_to_create = []
        for order in orders:
            lines_to_create.append({
                'wizard_id': self.id,
                'sale_id': order.id,
                'sale_name': order.name or '',
                'sale_state': order.state,
                'sale_invoice_status': order.invoice_status,
                'partner_name': order.partner_id.name or '',
                'company_name': order.company_id.name or '',
                })
        if not lines_to_create:
            return

        self.env['jap.sale.orders.same.partner.wizard.line'] \
            .create(lines_to_create)

    def action_open(self):
        self.ensure_one()
        self.sudo()._fill_lines()

        form = self.env.ref('jap_sale.jap_sale_orders_same_partner_wizard_form')
        return {
            'type': 'ir.actions.act_window',
            'name': _("Sale orders with the same customer"),
            'res_model': self._name,
            'view_mode': 'form',
            'views': [(form.id, 'form')],
            'target': 'new',
            'res_id': self.id,
            }


class JapSaleOrdersSamePartnerWizardLine(models.TransientModel):
    _name = "jap.sale.orders.same.partner.wizard.line"
    _description = "Line of Sale orders with the same customer"

    wizard_id = fields.Many2one(
        'jap.sale.orders.same.partner.wizard', 
        required=True, ondelete='cascade')
    sale_id = fields.Many2one(
        'sale.order',
        string='Order', readonly=True)
    sale_name = fields.Char(string='Order name', readonly=True)
    sale_state = fields.Char(string='Status', readonly=True)
    sale_invoice_status = fields.Char(string='Invoice status', readonly=True)
    partner_name = fields.Char(string='Customer', readonly=True)
    company_name = fields.Char(string='Company', readonly=True)

    def action_open_selected_sale_order(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale Order',
            'res_model': 'sale.order',
            'res_id': self.sale_id.id,
            'view_mode': 'form',
            'views': [(False, 'form')],
            'target': 'current',
            }
