# -*- coding: utf-8 -*-
from odoo import fields, models
from odoo.exceptions import UserError


class JapAddonsConfig(models.Model):
    _name = 'jap.addons.config'
    _description = 'Jap Addons Configuration'

    name = fields.Char(readonly=True, required=True, copy=False)
    active = fields.Boolean(default=True)
    description = fields.Char(copy=False)
    note = fields.Text(string="Notes", copy=False)

    _sql_constraints = [
        ('name', 'unique(name)', 'Name must be unique!'),
        ]

    def copy(self, default=None):
        raise UserError('Not allowed: copy a Jap Addons Configuration.')
