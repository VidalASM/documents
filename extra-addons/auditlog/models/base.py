# Copyright 2015 ABF OSIELL <https://osiell.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models
from odoo.exceptions import UserError

import logging 
from odoo.addons.smile_log.tools import SmileDBLogger
_logger = logging.getLogger(__name__)

class Base(models.AbstractModel):
    _inherit = 'base'

    @api.model
    def web_search_read(self, domain=None, fields=None, offset=0, limit=None, order=None, count_limit=None):
        """
        Override : Add logs handler to the action of searching data
        """
        _logger.info('You need ------------->. %s' %(str(domain)))
        ctx = self._context.get('params', False)
        rule = self.env['auditlog.rule'].search([('model_id.model','=','documents.document')], limit=1)
        model_name = ctx['model'] if ctx and 'model' in ctx else ''
        action_id = ctx['action'] if ctx and 'action' in ctx else 0
        logger = SmileDBLogger(self._cr.dbname, model_name, action_id, self._uid)
        dom = str(domain) if domain else ''
        logger.info("Busqueda de registros --> %s" %(dom))
        if model_name == 'documents.document' and rule:
            res_name = 'Search document'
            model_id = rule.pool._auditlog_model_cache['documents.document']
            res_id = 0
            method = 'search'
            uid = self._uid
            http_request_model = self.env["auditlog.http.request"]
            http_session_model = self.env["auditlog.http.session"]
            vals = {
                "name": res_name,
                "model_id": model_id,
                "res_id": res_id,
                "method": method,
                "user_id": uid,
                "log_type": rule.log_type,
                "http_request_id": http_request_model.current_http_request(),
                "http_session_id": http_session_model.current_http_session(),
            }
            log = self.env["auditlog.log"].create(vals)
            log_vals = {
                "field_id": 1,
                "log_id": log.id,
                "old_value": False,
                "old_value_text": False,
                "new_value": str(domain),
                "new_value_text": str(domain),
            }
            self.env["auditlog.log.line"].create(log_vals)
            # rule.create_logs(uid=self._uid, res_model='documents.document', res_ids=0, method='search')

        return super(Base, self).web_search_read(domain, fields, offset, limit, order, count_limit)

class Module(models.Model):
    _inherit = "ir.module.module"

    def download(self, download=True):
        """
        Override : Add logs handler to the action of searching data
        """
        logger = SmileDBLogger(self._cr.dbname, 'base', self._context.get('active_model'), self._uid)
        logger.info("BDescarga --> " )

        return super(Module, self).download(download)
    
