# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    analytic_id = fields.Many2one(
        'account.analytic.account',
        string='Cuenta Analítica')
    
class ProductProduct(models.Model):
    _inherit = 'product.product'

    analytic_id = fields.Many2one(
        related='product_tmpl_id.analytic_id')
