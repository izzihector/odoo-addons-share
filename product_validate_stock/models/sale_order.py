# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields, _
from odoo.exceptions import UserError, AccessError, ValidationError
import unicodedata
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, float_compare

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.onchange('product_uom_qty', 'product_uom', 'route_id')
    def _onchange_product_id_check_availability(self):
        if not self.product_id or not self.product_uom_qty or not self.product_uom:
            self.product_packaging = False
            return {}
        if self.product_id.type == 'product' and self.product_id.stock_validate:
            precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
            product_qty = self.product_uom._compute_quantity(self.product_uom_qty, self.product_id.uom_id)
            if float_compare(self.product_id.virtual_available, product_qty, precision_digits=precision) == -1:
                is_available = self._check_routing()
                if not is_available:
                    warning_mess = {
                        'title': _('Not enough inventory!'),
                        'message': _(
                            'You plan to sell %s %s but you only have %s %s available!\nThe stock on hand is %s %s.') % \
                                   (self.product_uom_qty, self.product_uom.name, self.product_id.virtual_available,
                                    self.product_id.uom_id.name, self.product_id.qty_available,
                                    self.product_id.uom_id.name)
                    }
                    return {'warning': warning_mess}
        return {}