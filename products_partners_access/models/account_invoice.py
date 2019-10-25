# coding: utf-8
from odoo import api, models

from .deny_access import deny_access


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(AccountInvoice, self).fields_view_get(view_id=view_id,
                                                          view_type=view_type,
                                                          toolbar=toolbar,
                                                          submenu=submenu)
        if view_type == 'form':
            if not self.env.user.partner_access:
                res['arch'] = deny_access(res['arch'], '//field[@name="partner_id"]')
            if not self.env.user.product_access:
                res['fields']['invoice_line_ids']['views']['tree']['arch'] = deny_access(res['fields']['invoice_line_ids']['views']['tree']['arch'], '//field[@name="product_id"]')
            if not self.env.user.account_access:
                res['fields']['invoice_line_ids']['views']['tree']['arch'] = deny_access(res['fields']['invoice_line_ids']['views']['tree']['arch'], '//field[@name="account_id"]')
                res['fields']['invoice_line_ids']['views']['tree']['arch'] = deny_access(res['fields']['invoice_line_ids']['views']['tree']['arch'], '//field[@name="account_analytic_id"]')
                res['fields']['tax_line_ids']['views']['tree']['arch'] = deny_access(res['fields']['tax_line_ids']['views']['tree']['arch'], '//field[@name="account_id"]')
                res['fields']['tax_line_ids']['views']['tree']['arch'] = deny_access(res['fields']['tax_line_ids']['views']['tree']['arch'], '//field[@name="account_analytic_id"]')
            if not self.env.user.user_access:
                res['arch'] = deny_access(res['arch'], '//field[@name="user_id"]')
        return res
