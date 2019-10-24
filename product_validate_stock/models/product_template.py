# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval
from datetime import datetime


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    stock_validate = fields.Boolean('Validar Stock')