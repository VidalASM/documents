#-*- coding:utf-8 -*-
{
    'name': "RP Database Size",
    'version': '13.0.1.0.1',
    'description': "Database Size",
    'summary': 'This module helps to show size of current postgres database.',
    'author': 'RP Odoo Developer',
    'category': 'Web',
    'license': "AGPL-3",
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_company.xml',
    ],
    'images': [
        'static/description/banner.png',
    ],
    'installable': True,
}
