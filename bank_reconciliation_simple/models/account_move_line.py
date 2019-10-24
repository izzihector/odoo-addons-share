# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountMoveLineRec(models.Model):
    """."""

    _inherit = "account.move.line"

    reconciled = fields.Boolean('Conciliado', readonly=True)
    can_be_reconciled = fields.Boolean(
        'Conciliable', related='account_id.simple_reconcilliation')
