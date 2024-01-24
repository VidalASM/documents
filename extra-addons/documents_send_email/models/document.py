from odoo import models, fields, api, _

class Document(models.Model):
    _inherit = 'documents.document'

    @api.model
    def get_send_mail_details(self):
        template_id = False
        if not template_id:
            template_id = self.env['ir.model.data']._xmlid_to_res_id('documents_send_email.email_template_documents', raise_if_not_found=False)
        return {
            'template_id': template_id,
            'company_id': self.env.company.id,
            'company_name': self.env.company.name,
            'author_name': self.env.user.partner_id.name,
            'email_from': self.env.user.partner_id.email,
            'reply_to': self.env.user.partner_id.email,
        }