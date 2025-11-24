# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'JAP Sales',
    'summary': "Improvements to Sales Orders",
    'version': '18.0.1.0.0',
    'description': "Allows creating invoices from selected sale order lines",
    'author': 'japinol',
    'company': 'japinol',
    'website': '',
    'category': 'Sales',
    'depends': [
        'sale',
        'jap_addons_config',
    ],
    'data': [
        'data/jap_addons_config.xml',
        'security/ir.model.access.csv',
        'views/jap_addons_config_view.xml',
        'views/sale_order_view.xml',
        'views/account_move_view.xml',
        'wizard/create_invoice_from_sel_sale_lines_wizard.xml',
        'wizard/sale_orders_same_partner_wizard.xml',
    ],
    'demo': [],
    'images': [],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
