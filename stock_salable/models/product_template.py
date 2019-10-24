# coding: utf-8
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.depends('qty_available', 'outgoing_qty')
    def _compute_stock_salable(self):
        """ Calculates salable stock, defined as ``stock - outgoing`` """
        for prod in self:
            prod.qty_salable = prod.qty_available - prod.outgoing_qty

    qty_salable = fields.Float('Stock Salable', compute=_compute_stock_salable,
                               help='Amount of products available - outgoing quantity')


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.depends('qty_available', 'outgoing_qty')
    def _compute_stock_salable(self):
        """ Calculates salable stock, defined as ``stock - outgoing`` """
        for prod in self:
            prod.qty_salable = prod.qty_available - prod.outgoing_qty

    qty_salable = fields.Float('Stock Salable', compute=_compute_stock_salable,
                               help='Amount of products available - outgoing quantity')
