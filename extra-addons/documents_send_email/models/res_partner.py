from odoo import api, fields, models, _
from odoo.tools import html_escape

class ResPartner(models.Model):
    _inherit = 'res.partner'

    def documents_message_post(self,attachment_ids=None):
        self.ensure_one()
        if self.ids:
            attachments = self.env['ir.attachment'].sudo().browse(attachment_ids)
            message = _('<p>Documents : Send by Email </p>')
            for attachment in attachments:
                message += '<p>%s</p><br/>' % html_escape(attachment.name)
            self.message_post(body=message, partner_ids=self.ids or [])