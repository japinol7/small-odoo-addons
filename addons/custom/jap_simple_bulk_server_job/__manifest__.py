# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'JAP Simple Bulk Server Job',
    'summary': "JAP Simple Bulk Server Job",
    'version': '19.0.1.1.1',
    'description': """
JAP Simple Bulk Server Job
==========================
A Technical addon intended to be used by System Administrators.

This addon allows creating special jobs able to process several records in bulk; 
a batch of N items per cron execution. 

It includes a Wizard to create jobs, views to manage them and a cron to execute the jobs.
* All the menus and views can be accessed from this menu:
Settings -- Technical -- Jap. Addons

..
Current limitations of the 'JAP Simple Bulk Server Job':

The current implementation guarantees that each invocation of the cron
selects at most one job.
It does not guarantee that two concurrent cron invocations cannot select the same job.

This implementation assumes that your Odoo deployment will run only 
one instance of the cron '_cron_process_items_bulk_processing_job' at a time.
    """,
    'author': 'japinol',
    'company': 'japinol',
    'website': '',
    'category': 'Technical',
    'depends': [
        'jap_addons_config',
    ],
    'data': [
        'data/cron.xml',
        'security/ir.model.access.csv',
        'views/jap_addons_config_view.xml',
        'views/jap_simple_bulk_server_job_menu.xml',
        'views/jap_simple_bulk_server_job_view.xml',
        'wizard/jap_simple_bulk_server_job_wizard.xml',
    ],
    'demo': [],
    'images': [],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
