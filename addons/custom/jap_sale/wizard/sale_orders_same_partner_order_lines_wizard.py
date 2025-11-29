# -*- coding: utf-8 -*-
from odoo import models, fields, _

import logging

_logger = logging.getLogger(__name__)


class JapSaleOrdersSamePartnerOrderLinesWizard(models.TransientModel):
    _name = "jap.sale.orders.same.partner.order.lines.wizard"
    _description = "Sale order lines - From Sale orders with the same customer"

    sale_id = fields.Many2one(
        'sale.order',
        string='Sale', readonly=True)
    partner_name = fields.Char(string='Customer', readonly=True)
    line_ids = fields.One2many(
        'jap.sale.orders.same.partner.order.lines.wizard.line',
        inverse_name='wizard_id',
        string="Matches", readonly=True)

    def _fill_lines(self):
        self.ensure_one()
        self.line_ids.unlink()

        if not self.sale_id:
            return

        order_lines = self.env['sale.order.line'].sudo().search([
            ('order_id', '=', self.sale_id.id),
            ], order='id desc')

        lines_to_create = []
        for order_line in order_lines:
            lines_to_create.append({
                'wizard_id': self.id,
                'sale_line_id': order_line.id,
                'product_id': order_line.product_id.id,
                'product_uom_qty': order_line.product_uom_qty,
                'qty_to_invoice': order_line.qty_to_invoice,
                'currency_id': order_line.currency_id.id,
                'price_unit': order_line.price_unit,
                'discount': order_line.discount,
                'price_subtotal': order_line.price_subtotal,
                'price_total': order_line.price_total,
                })
        if not lines_to_create:
            return

        self.env['jap.sale.orders.same.partner.order.lines.wizard.line'] \
            .create(lines_to_create)

    def action_open(self):
        self.ensure_one()
        self.sudo()._fill_lines()

        form = self.env.ref('jap_sale.jap_sale_orders_same_partner_order_lines_wizard_form')
        return {
            'type': 'ir.actions.act_window',
            'name': _("Sale order lines - From Sale orders with the same customer"),
            'res_model': self._name,
            'view_mode': 'form',
            'views': [(form.id, 'form')],
            'target': 'new',
            'res_id': self.id,
            }

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

    def action_return(self):
        self.ensure_one()
        parent_wizard = self.env['jap.sale.orders.same.partner.wizard'].create({
            'partner_id': self.sudo().sale_id.partner_id.id,
            })
        return parent_wizard.action_open()


class JapSaleOrdersSamePartnerOrderLinesWizardLine(models.TransientModel):
    _name = "jap.sale.orders.same.partner.order.lines.wizard.line"
    _description = "Line of Sale order lines - From Sale orders with the same customer"

    wizard_id = fields.Many2one(
        'jap.sale.orders.same.partner.order.lines.wizard',
        required=True, ondelete='cascade')
    sale_line_id = fields.Many2one(
        'sale.order.line',
        string='Order Line', readonly=True)
    product_id = fields.Many2one(
        'product.product',
        string='Product', readonly=True)
    product_uom_qty = fields.Float(
        string="Qty Ordered", readonly=True)
    qty_to_invoice = fields.Float(
        string="Qty To Invoice", readonly=True)
    currency_id = fields.Many2one(
        'res.currency', string="Currency",
        help='The currency used to enter statement')
    price_unit = fields.Float(
        string="Unit Price", aggregator='avg', readonly=True)
    discount = fields.Float(
        string="Discount %", readonly=True, aggregator='avg')
    price_subtotal = fields.Monetary(
        string="Untaxed Total", readonly=True)
    price_total = fields.Monetary(
        string="Total", readonly=True)
