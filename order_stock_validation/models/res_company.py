# -*- coding: utf-8 -*-

from odoo import fields, models


class Company(models.Model):
    """."""

    _inherit = 'res.company'

    sale_validate_pickings = fields.Boolean(
        'Validar facturación en ventas', default=True,
        help='Validar albaranes al facturar pedidos de ventas')
    purchase_validate_pickings = fields.Boolean(
        'Validar facturación en compras', default=True,
        help="Validar albaranes al facturar pedidos de compras")
