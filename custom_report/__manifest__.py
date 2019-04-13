# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Custom Report Template',
    'summary': """Custom Report Template""",
    'description': """
        Custom report template. Separate header and footer with custom design.\n
        Developed by Jeshad Khan
    """,
    'version': '1.0',
    'author': 'Metamorphosis',
    'company': 'Metamorphosis Limited',
    'website': 'metamorphosis.com.bd',
    'category': 'Report',
    'depends': ['base', 'report'],
    'data': [
        'data/report_paperformat_data.xml',
        'layout/custom_report_header_footer.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
