# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'JAP Addons Config',
    'summary': "Configuration options for Jap addons",
    'version': '16.0.1.0.0',
    'description': "Configuration options for Jap addons",
    'author': 'japinol',
    'company': 'japinol',
    'website': '',
    'category': 'Custom',
    'depends': [
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/jap_addons_config.xml',
        'views/jap_addons_config_menu.xml',
        'views/jap_addons_config_view.xml',
    ],
    'demo': [],
    'images': [],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
