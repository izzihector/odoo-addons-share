# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    
    commission_type = fields.Selection([
        ('0', "Producto/Cliente"),
        ('1', "Producto/Vendedor"),
        ], string="Variables a usar en cálculo de comisión",
        default='0', config_parameter='sale_commission_report.commission_type')
