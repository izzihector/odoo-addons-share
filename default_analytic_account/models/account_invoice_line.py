# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class AccountInvoiceLineAnalytic(models.Model):
    _inherit = "account.invoice.line"

    @api.onchange('product_id')
    def _onchange_product_id(self):
        res = super(AccountInvoiceLineAnalytic, self)._onchange_product_id()
        self.account_analytic_id = self.product_id.analytic_id and self.product_id.analytic_id.id or self.partner_id.analytic_id.id
        return res
