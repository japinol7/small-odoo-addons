# -*- coding: utf-8 -*-
from odoo import models, fields
from odoo.exceptions import ValidationError


class JapResUsersCleanPermissionGroups(models.TransientModel):
    """This wizard allows to clean user permission groups."""

    _name = "jap.res.users.clean.permission.groups.wizard"
    _description = "Clean User Permission Groups"

    def _default_user_id(self):
        context = self.env.context
        if context.get('active_model') != 'res.users':
            raise ValidationError('Active_model should be res.users!')

        active_id = context.get('active_id')
        if not active_id:
            raise ValidationError('Missing active_id in context!')

        return self.env['res.users'].browse(active_id)[0]

    user_id = fields.Many2one(
        'res.users', string='User', readonly=True,
        default=_default_user_id)
    user_name = fields.Char(
        string='User Name', readonly=True, translate=True)
    user_login = fields.Char(
        string='Login', readonly=True, translate=True)

    def clean_user_permission_groups_confirm(self):
        self.ensure_one()
        self.user_id.write({
            'groups_id': [(5, self.env.ref('base.group_user').id)],
            })

        return {'type': 'ir.actions.client', 'tag': 'soft_reload'}
