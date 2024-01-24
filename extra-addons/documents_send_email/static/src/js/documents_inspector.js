/** @odoo-module */

import { DocumentsInspector } from "@documents/views/inspector/documents_inspector";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { FormViewDialog } from '@web/views/view_dialogs/form_view_dialog';
import { session } from "@web/session";


var Dialog = require('web.Dialog');
var core = require('web.core');
var _t = core._t;


patch(DocumentsInspector.prototype, 'on_shared_users', {
    setup() {
        this._super(...arguments);
        this.orm = useService("orm");
        this.dialogService = useService("dialog");
        this.actionService = useService("action");
    },

    async _onSendEmail(ev){
        ev.preventDefault();
        ev.stopPropagation();

        let self = this;
        
        if (!this.props.selection.length) {
            return;
        }

        if (this.props.selection.length >= 1){
            var attachment_ids = [];
            var res_ids = [];
            var default_partner_ids = [];
            for(var i = 0, l = this.props.selection.length; i < l; ++i) {
                if(!this.props.selection[i].data.url){
                    if (this.props.selection[i].data) {
                        if (this.props.selection[i].data.res_id != undefined){
                            res_ids.push(this.props.selection[i].data.res_id);
                        }
                        if (this.props.selection[i].data.attachment_id && this.props.selection[i].data.attachment_id[0] != undefined){
                            attachment_ids.push(this.props.selection[i].data.attachment_id[0]);
                        }
                        if (this.props.selection[i].data.partner_id && this.props.selection[i].data.partner_id[0] != undefined){
                            default_partner_ids.push(this.props.selection[0].data.partner_id[0]);
                        }
                    }
                }
            }

            return await self.orm.silent.call('documents.document','get_send_mail_details').then(function(res) {
                const action = {
                    name: _t("Compose Email"),
                    type: 'ir.actions.act_window',
                    res_model: 'mail.compose.message',
                    views: [[false, 'form']],
                    target: 'new',
                    context: {
                        'default_model': 'res.partner',
                        'default_company_id': res['company_id'],
                        'default_company_name': res['company_name'],
                        'default_author_name': res['author_name'],
                        'default_email_from': res['email_from'],
                        'default_reply_to': res['reply_to'],
                        'default_partner_ids': default_partner_ids,
                        'default_template_id': res['template_id'],
                        'default_composition_mode': 'comment',
                        'default_attachment_ids': attachment_ids,
                        'default_res_id': res_ids[0],
                        'force_email': true,
                        'mail_post_autofollow': true,
                    },
                };
                self.actionService.doAction(action).then(async function(){
                    if (attachment_ids && attachment_ids[0] ){
                        await self.orm.silent.call('res.partner','documents_message_post',[[default_partner_ids[0]],attachment_ids])
                    }
                });
            });
        }
    }
});