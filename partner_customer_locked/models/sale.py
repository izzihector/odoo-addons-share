# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        context = self._context
        res = {}
        if not 'hide_sale' in context:
            if self.partner_id.account_filter == 'bloqueado':
                partner_name = self.partner_id.name.encode('utf-8').strip()
                warning = {
                    'title': ("Aviso"),
                    'message': '{0} se encuentra (bloqueado)'.format(partner_name)
                    }
                res['warning'] = warning
                self.partner_id = False
                return res
        return super(SaleOrder, self).onchange_partner_id()