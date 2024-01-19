# -*- coding: utf-8 -*-
{
    'name': "Import Export Document Log Report",

    'summary': """
        Document Log Report with total initial, qty in, qty out, balance""",

    'description': """
        
    """,
    "license": "LGPL-3",
    'author': "Jason Vu",
    'website': "https://github.com/longvm91/odoo-custom-modules/tree/16.0/imex_inventory_report",
    'email': "longvm91@gmail.com",
    'category': 'Warehouse',
    'version': '16.0.1.3.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'documents'],

    # always loaded
    'data': [
        'reports/document_log_report_views.xml',
        'reports/document_log_details_report_views.xml',
        'wizard/document_log_report_wizard_view.xml',
        'security/ir.model.access.csv',
    ],
    'images': ['static/img/report1.png', 'static/img/report2.png'],
    "assets": {
        "web.assets_backend": [
            "document_log_report/static/src/css/**/*",
            "document_log_report/static/src/js/**/*",
        ],
    },
    "installable": True,
}
