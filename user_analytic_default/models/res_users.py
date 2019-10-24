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

class ResUsers(models.Model):
    _inherit = "res.users"

    waiter_user = fields.Boolean('waiter_user')
    
    account_analytic = fields.Many2one(
        'account.analytic.account', 
        string='Cuenta Analítica Usuario')
