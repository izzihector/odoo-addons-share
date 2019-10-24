# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountAccountRec(models.Model):
    """."""

    _inherit = "account.account"

    simple_reconcilliation = fields.Boolean('Conciliar Simple')
