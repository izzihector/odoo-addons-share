# -*- coding: utf-8 -*-

import unicodedata

from odoo import api, fields, models


class ResPartner(models.Model):
    """."""

    _inherit = 'res.partner'

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

    @api.onchange('ref')
    def ref_capital(self):
        """."""
        if self.company_id.capital_text and self.ref:
            temp_value = self.ref.upper()
            if self.company_id.acento_text:
                temp_value = ''.join((c for c in unicodedata.normalize(
                    'NFD', temp_value) if unicodedata.category(c) != 'Mn'))
            self.ref = temp_value

    @api.onchange('giro')
    def giro_capital(self):
        """."""
        if self.company_id.capital_text and self.giro:
            temp_value = self.giro.upper()
            if self.company_id.acento_text:
                temp_value = ''.join(
                    (c for c in unicodedata.normalize(
                        'NFD', temp_value) if unicodedata.category(c) != 'Mn'))
            self.giro = temp_value

    @api.onchange('city')
    def city_capital(self):
        """."""
        if self.company_id.capital_text and self.city:
            temp_value = self.city.upper()
            if self.company_id.acento_text:
                temp_value = ''.join(
                    (c for c in unicodedata.normalize(
                        'NFD', temp_value) if unicodedata.category(c) != 'Mn'))
            self.city = temp_value

    @api.onchange('street')
    def street_capital(self):
        """."""
        if self.company_id.capital_text and self.street:
            temp_value = self.street.upper()
            if self.company_id.acento_text:
                temp_value = ''.join(
                    (c for c in unicodedata.normalize(
                        'NFD', temp_value) if unicodedata.category(c) != 'Mn'))
            self.street = temp_value

    @api.onchange('street2')
    def street2_capital(self):
        """."""
        if self.company_id.capital_text and self.street2:
            temp_value = self.street2.upper()
            if self.company_id.acento_text:
                temp_value = ''.join(
                    (c for c in unicodedata.normalize(
                        'NFD', temp_value) if unicodedata.category(c) != 'Mn'))
            self.street2 = temp_value
