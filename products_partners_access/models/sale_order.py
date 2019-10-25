# coding: utf-8
from odoo import api, models

from .deny_access import deny_access


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(SaleOrder, self).fields_view_get(view_id=view_id,
                                                     view_type=view_type,
                                                     toolbar=toolbar,
                                                     submenu=submenu)
        if view_type == 'form':
            if not self.env.user.partner_access:
                res['arch'] = deny_access(res['arch'], '//field[@name="partner_id"]')
            if not self.env.user.product_access:
                res['fields']['order_line']['views']['tree']['arch'] = deny_access(res['fields']['order_line']['views']['tree']['arch'], '//field[@name="product_id"]')
                res['fields']['order_line']['views']['form']['arch'] = deny_access(res['fields']['order_line']['views']['form']['arch'], '//field[@name="product_id"]')
            if not self.env.user.account_access:
                res['arch'] = deny_access(res['arch'], '//field[@name="project_id"]')
                res['fields']['order_line']['views']['tree']['arch'] = deny_access(res['fields']['order_line']['views']['tree']['arch'], '//field[@name="analytic_tag_ids"]')
            if not self.env.user.user_access:
                res['arch'] = deny_access(res['arch'], '//field[@name="user_id"]')
        return res
