# -*- coding: utf-8 -*-

import unicodedata

from odoo import api, fields, models


class ProductTemplate(models.Model):
    """."""

    _inherit = 'product.template'

    company_id = fields.Many2one(
        'res.company', string="Company", required=True,
        default=lambda self: self.env.user.company_id.id)

    @api.onchange('name')
    def name_capital(self):
        """."""
        if self.company_id.capital_text and self.name:
            temp_value = self.name.upper()
            if self.company_id.acento_text:
                temp_value = ''.join((c for c in unicodedata.normalize(
                    'NFD', temp_value) if unicodedata.category(c) != 'Mn'))
            self.name = temp_value
