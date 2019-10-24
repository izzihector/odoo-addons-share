# -*- coding: utf-8 -*-

from odoo import fields, models, api

class ResCompany(models.Model):
    _inherit = "res.company"

    days = fields.Integer(string='Cantidad de dias', 
                          default=0,
                          help='Ingrese la cantidad de dias que despues de vencida la factura el cliente se bloqueara automaticamente', 
                          required=True)