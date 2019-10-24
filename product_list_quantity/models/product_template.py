# -*- coding: utf-8 -*-

from odoo import fields, models


class ProductTemplateList(models.Model):
    """."""

    _name = 'product.template.product.list'
    _description = 'Lista de productos relacionados'

    product_id = fields.Many2one(
        'product.product', 'Producto', required=True)

    product_tmpl_id = fields.Many2one(
        'product.template', 'Plantilla de producto', required=True)

    qty_available = fields.Float(
        'Cantidad', related='product_id.qty_available')


class ProductTemplate(models.Model):
    """."""

    _inherit = 'product.template'

    product_list_ids = fields.One2many(
        'product.template.product.list', 'product_tmpl_id',
        'Listado de productos relacionados')
