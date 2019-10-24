# coding: utf-8
from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    can_delete_customers = fields.Boolean(default=True)
    can_delete_suppliers = fields.Boolean(default=True)
