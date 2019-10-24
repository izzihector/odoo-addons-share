# coding: utf-8
from odoo import api, fields, models


class ProductTag(models.Model):
    _name = 'product.tag'
    _description = 'Product Tags'

    active = fields.Boolean(default=True)
    color = fields.Integer(required=True, default=0)
    name = fields.Char(required=True)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    other_price = fields.Float('Other Price')
