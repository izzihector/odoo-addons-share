# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO, Open Source Management Solution
#    Copyright (C) 2016 Steigend IT Solutions
#    For more details, check COPYRIGHT and LICENSE files
#
##############################################################################
from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp

class AnalyticPartner(models.Model):
    _inherit = "res.partner"

    analytic_id = fields.Many2one(
        'account.analytic.account', 
        string='Cuenta Analítica')
