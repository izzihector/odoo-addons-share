# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.onchange('partner_id', 'company_id')
    def _onchange_partner_id(self):
        res = {}
        context = self._context
        type = context.get('type')
        if self.partner_id.account_filter == 'bloqueado' and type == 'out_invoice':
            partner_name = self.partner_id.name.encode('utf-8').strip()
            self.partner_id = False
            warning = {
                    'title': ("Aviso"),
                    'message': '{0} se encuentra (bloqueado)'.format(partner_name)
                    }
            res['warning'] = warning
            return res
        invoice = super(AccountInvoice, self)._onchange_partner_id()
        return invoice
        
        
        