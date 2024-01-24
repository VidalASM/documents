# -*- coding: utf-8 -*-
#################################################################################
# Author      : CFIS (<https://http://www.cfis-apps.com>)
# Copyright(c): 2017-Present CFIS.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://http://www.cfis-apps.com>
#################################################################################

{
    "name": "Send Document | Document Send by Email",
    "summary": """
        This module offers easy-to-use capability for sending documents from the documents module. Additionally, 
        if you navigate to the partners' documents and send documents as email, this module will record the message. 
    """,
    "version": "16.0.1",
    "description": """
        This module offers easy-to-use capability for sending documents from the documents module. Additionally, 
        if you navigate to the partners' documents and send documents as email, this module will record the message. 
    """,    
    "author": "CFIS",
    "maintainer": "CFIS",
    "license" :  "Other proprietary",
    "website": "https://www.cfis-apps.com",
    "images": ["images/documents_send_email.png"],
    "category": "Sales",
    "depends": [
        "base",
        "mail",
        "documents"
    ],
    "data": [
        "data/mail_attachment_data.xml",  
    ],
    "assets": {
        "web.assets_backend": [
            "/documents_send_email/static/src/js/*.js",
            "/documents_send_email/static/src/xml/*.xml",
        ],
    },    
    "installable": True,
    "application": True,
    "price"                 :  20,
    "currency"              :  "EUR",
    "pre_init_hook"         :  "pre_init_check",
}
