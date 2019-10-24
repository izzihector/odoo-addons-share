# -*- coding: utf-8 -*-

from odoo import fields, models


class Company(models.Model):
    """."""

    _inherit = 'res.company'

    capital_text = fields.Boolean(
        'Colocar los textos en mayúsculas',
        help="Coloca/Quita los textos en mayúsculas",
        default=False)
    acento_text = fields.Boolean(
        'No usar acentos',
        help="Coloca/Quita los Acentos",
        default=False)
