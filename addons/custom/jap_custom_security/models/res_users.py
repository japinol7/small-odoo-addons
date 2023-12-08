# -*- coding: utf-8 -*-
from odoo import models
from odoo.tools.safe_eval import safe_eval


class ResUsers(models.Model):
    _inherit = 'res.users'

    def action_jap_res_users_clean_permission_groups(self):
        self.ensure_one()
        res = self.env['ir.actions.act_window']._for_xml_id(
            'jap_custom_security.action_jap_res_users_clean_permission_groups_wizard')
        res['context'] = safe_eval(res['context']) if res.get('context') else {}
        res['context'].update({
            'default_user_id': self.id,
            'default_user_name': self.name,
            'default_user_login': self.login,
            })
        return res
