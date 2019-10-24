# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    @api.onchange('partner_id')
    def _get_default_analytic(self):
        user = self.env.user
        self.analytic_account_id = user.account_analytic.id
        
class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    @api.multi

    def _prepare_invoice_line(self, qty):
        user = self.env.user
        res = super(SaleOrderLine, self)._prepare_invoice_line(qty)
        if not self.order_id.analytic_account_id:
            default_analytic_account = user.account_analytic.id or self.order_id.partner_id.analytic_id and self.order_id.partner_id.analytic_id.id or self.product_id.analytic_id.id
            self.order_id.analytic_account_id = default_analytic_account
            if default_analytic_account:
                res.update({'account_analytic_id': default_analytic_account})
        return res
