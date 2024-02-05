# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


import logging 
# from odoo.addons.smile_log.tools import SmileDBLogger
_logger = logging.getLogger(__name__)

class DiscussController(WebsiteSale):
    @http.route('/mail/channel/<int:channel_id>/attachment/<int:attachment_id>', methods=['GET'], type='http', auth='public')
    def mail_channel_attachment(self, channel_id, attachment_id, download=None, **kwargs):
        res = super(DiscussController, self).mail_channel_attachment(channel_id, attachment_id, download, **kwargs)
        # logger = SmileDBLogger(self._cr.dbname, 'base', 1, self._uid)
        # logger.info("Download ------------->")
        _logger.info('You need ------------->.')
        # channel_member_sudo = request.env['mail.channel.member']._get_as_sudo_from_request_or_raise(request=request, channel_id=int(channel_id))
        # attachment_sudo = channel_member_sudo.env['ir.attachment'].search([
        #     ('id', '=', int(attachment_id)),
        #     ('res_id', '=', int(channel_id)),
        #     ('res_model', '=', 'mail.channel')
        # ], limit=1)
        # if not attachment_sudo:
        #     raise NotFound()
        # return request.env['ir.binary']._get_stream_from(attachment_sudo).get_response(as_attachment=download)
        return res