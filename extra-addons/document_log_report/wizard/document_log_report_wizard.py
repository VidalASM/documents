# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval


class DocumentLogReportWizard(models.TransientModel):
    _name = "document.log.report.wizard"
    _description = "Document Log Report Wizard"

    date_from = fields.Date(string="Start Date")
    date_to = fields.Date(string="End Date")
    user_ids = fields.Many2many(
        comodel_name="res.users", string="User")
    document_ids = fields.Many2many(
        comodel_name="documents.document", string="Document")
    
    def _prepare_document_log_report(self):
        # users = self.user_ids if self.user_ids else 
        return {
            "date_from": self.date_from or "1900-01-01",
            "date_to": self.date_to or fields.Date.context_today(self),
            "user_ids": [(6, 0, self.user_ids.ids)] if self.user_ids else [(6, 0, self.env['res.users'].search([]).ids)],
            "document_ids": [(6, 0, self.document_ids.ids)] if self.document_ids else [(6, 0, self.env['documents.document'].search([]).ids)],
        }

    def button_view(self):
        vals = {}
        report = self.create(self._prepare_document_log_report())

        self.env["document.log.report"].init_results(report)
        action = self.env.ref(
            "document_log_report.action_document_log_report_tree_view")
        vals = action.sudo().read()[0]
        context = vals.get("context", {})
        if context:
            context = safe_eval(context)
        context["filters"] = self._prepare_document_log_report()
        vals["context"] = context
        return vals

    # def button_view_details(self):
    #     vals = {}
    #     report = self.create(self._prepare_document_log_report())
    #     init = self.env["document.log.details.report"].init_results(report)
    #     details = self.env["document.log.details.report"].search([])
    #     action = self.env.ref(
    #         'document_log_report.action_document_log_details_report')
    #     vals = action.sudo().read()[0]
    #     context = vals.get("context", {})
    #     if context:
    #         context = safe_eval(context)
    #     context["active_ids"] = details.ids
    #     data = {
    #         'product_default_code': self.product_ids.default_code,
    #         'product_name': self.product_ids.name,
    #         'date_from': self.date_from or None,
    #         'date_to': self.date_to or fields.Date.context_today(self),
    #         'location': self.location_id.complete_name or None,
    #         'category': self.product_ids.categ_id.complete_name or None,
    #     }
    #     context["data"] = data
    #     vals["context"] = context
    #     return vals
