# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class company_tax(models.Model):

    _description = "Company registered"
    _inherit = 'res.company'
  
        
    taxes_id = fields.Many2one("account.tax", 'Impuesto Venta')
