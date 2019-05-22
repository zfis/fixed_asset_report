# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Fixed Asset PDF Report',
    'summary': """Account Fixed Asset PDF Report""",
    'icon': "/fixed_asset_report/static/description/icon.png",
    "images": ["static/description/fixed_asset.png"],
    'description': """
        Fixed asset report of account. It's allow to generate fixed asset report.\n
        Developed by Jeshad Khan For Metamorphosis Ltd.
    """,
    'version': '10.0.1.0',
    'author': 'Metamorphosis',
    'company': 'Metamorphosis Limited',
    'website': 'metamorphosis.com.bd',
    'category': 'Accounting',
    'sequence': 7,
    'depends': ['base', 'account', 'account_asset', 'custom_report'],
    'data': [
        'data/ir_sequence.xml',
        'views/fixed_asset_report_filter_wizard_view.xml',
        'views/fixed_asset_form_view.xml',
        'report/fixed_asset_schedule_report.xml',
        'report/fixed_asset_register_report.xml'
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    "license": "OPL-1",
    "price": 79,
    "currency": "EUR",
}
