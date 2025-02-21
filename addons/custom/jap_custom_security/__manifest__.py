# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'JAP Security',
    'summary': "Customizes security and access permissions",
    'version': '18.0.1.0.0',
    'description': "Customizes security and access permissions",
    'author': 'japinol',
    'company': 'japinol',
    'website': '',
    'category': 'Custom',
    'depends': [
        'sale',
        'jap_addons_config',
        'jap_sale',
    ],
    'data': [
        'security/account_security.xml',
        'security/jap_groups.xml',
        'security/sale/ir.model.access.csv',
        'security/user/ir.model.access.csv',
        'data/jap_addons_config.xml',
        'views/jap_addons_config_view.xml',
        'views/res_users_view.xml',
        'views/sale_order_view.xml',
        'wizard/res_user_clean_permission_groups_wizard.xml',
    ],
    'demo': [],
    'images': [],
    'installable': True,
    'auto_install': True,
    'license': 'LGPL-3',
}
