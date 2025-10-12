# -*- coding: utf-8 -*-

from odoo import api, models
from .. import jap_custom_version


class JapCustomizeVersion(models.Model):
    _name = 'jap.customize.version'
    _description = 'Jap Customize Version'

    @api.model
    def get_jap_custom_version(self):
        return jap_custom_version.jap_custom_version
