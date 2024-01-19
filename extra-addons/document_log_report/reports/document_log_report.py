
from odoo import api, fields, models, tools
from odoo.tools.safe_eval import safe_eval


class DocumentLogReport(models.Model):
    _name = "document.log.report"
    _description = "Document Log Report"
    _auto = False

    document_id = fields.Many2one(comodel_name="documents.document", readonly=True)
    author_id = fields.Many2one(comodel_name="res.partner", readonly=True)
    message_type = fields.Selection([
        ('email', 'Email'),
        ('comment', 'Comment'),
        ('notification', 'System notification'),
        ('user_notification', 'User Specific Notification')],
        'Type', readonly=True)
    date = fields.Datetime('Date', readonly=True)
    body = fields.Html('Contents', sanitize_style=True)

    # TODO: need a field to help these cases more clearly
    # case 1: location set
    #       => count internal transfer and group by location
    #    1.1: group_location = True
    #       => select all child_of location
    #    1.2: group_location = False
    #       => select only location_id
    # case 2: location not set
    #       => select all internal locations
    #    2.1: group_location = True
    #       => count internal transfer and group by location
    #    2.2: group_location = False
    #       => not count internal transfer and neither group by location

    def init_results(self, filter_fields):
        date_from = filter_fields.date_from or "1900-01-01"
        date_to = filter_fields.date_to or fields.Date.context_today(self)

        query_ = """
            select mm.id, mm.message_type, mm.date, mm.body, dd.id as document_id, rp.id as author_id 
            from mail_message mm 
            left join documents_document dd on mm.res_id = dd.id 
            left join res_partner rp on mm.author_id = rp.id
            where mm.model = 'documents.document' and mm.date >= %s and mm.date <= %s
        """
        params = (date_from,
                    date_to)
        tools.drop_view_if_exists(self._cr, self._table)
        res = self._cr.execute(
            """CREATE VIEW {} as ({})""".format(self._table, query_), params)
        return res

    def report_details(self):
        vals = {}
        filters = self._context.get("filters")
        filters["product_ids"] = [(6, 0, self.product_id.ids)]
        report = self.env["document.log.report.wizard"].create(
            self._context.get("filters"))
        init = self.env["document.log.details.report"].init_results(report)
        details = self.env["document.log.details.report"].search([])
        action = self.env.ref(
            'document_log_report.action_document_log_details_report')
        vals = action.sudo().read()[0]
        context = vals.get("context", {})
        if context:
            context = safe_eval(context)
        context["active_ids"] = details.ids
        data = {
            'product_default_code': report.product_ids.default_code,
            'product_name': report.product_ids.name,
            'date_from': report.date_from or None,
            'date_to': report.date_to or fields.Date.context_today(self),
            'location': report.location_id.complete_name or None,
            'category': report.product_ids.categ_id.complete_name or None,
        }
        context["data"] = data
        vals["context"] = context
        return vals
