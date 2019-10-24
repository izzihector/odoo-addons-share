# coding: utf-8
from odoo import fields, models


class StockLocation(models.Model):
    _inherit = 'stock.location'

    salable_stock = fields.Boolean('Available on Salable Stock', default=True)
