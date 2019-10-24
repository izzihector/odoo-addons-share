# -*- coding: utf-8 -*-

from odoo import models, fields, api

AVAILABLE_FILTER = [('disponible', 'Disponible'),('bloqueado', 'Bloqueado'),]

class Partner(models.Model):
    _inherit = 'res.partner'

    account_filter = fields.Selection(selection=AVAILABLE_FILTER, string='Estatus', default='disponible')
    motive_locked  = fields.Char(string='Motivo', size=128)
