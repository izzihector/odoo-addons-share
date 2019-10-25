# coding: utf-8
from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    partner_access = fields.Boolean(default=True)
    product_access = fields.Boolean(default=True)
    account_access = fields.Boolean(default=True)
    user_access = fields.Boolean(default=True)
