# coding: utf-8
from odoo import api, models

from .deny_access import deny_access


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(StockPicking, self).fields_view_get(view_id=view_id,
                                                        view_type=view_type,
                                                        toolbar=toolbar,
                                                        submenu=submenu)
        if view_type == 'form':
            if not self.env.user.partner_access:
                res['arch'] = deny_access(res['arch'], '//field[@name="partner_id"]')
        return res


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(StockMove, self).fields_view_get(view_id=view_id,
                                                     view_type=view_type,
                                                     toolbar=toolbar,
                                                     submenu=submenu)
        if view_type == 'tree':
            if not self.env.user.product_access:
                res['arch'] = deny_access(res['arch'], '//field[@name="product_id"]')
        return res
