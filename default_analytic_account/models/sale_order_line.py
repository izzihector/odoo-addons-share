# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.multi
    def _prepare_invoice_line(self, qty):
        res = super(SaleOrderLine, self)._prepare_invoice_line(qty)
        if not self.order_id.analytic_account_id:
            default_analytic_account = self.product_id.analytic_id and self.product_id.analytic_id.id or self.order_id.partner_id.analytic_id.id
            if default_analytic_account:
                res.update({'account_analytic_id': default_analytic_account})
        return res
