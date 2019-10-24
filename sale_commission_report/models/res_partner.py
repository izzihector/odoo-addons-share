# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class ResPartnerType(models.Model):
    _description = "Partner Type"
    _name = 'res.partner.type'

    @api.multi
    def name_get(self):
        res = super(ResPartnerType, self).name_get()
        data = []
        for ptype in self:
            display_value = '(%r) %s'%(ptype.commission,ptype.name)
            data.append((ptype.id, display_value))
        return data
        
    name = fields.Char(string="Descripción",copy=False, required=True)
    commission = fields.Float('Comisión (%)', default=0.0)
    
    
class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def _get_partner_type(self):
        value = self.env['res.partner.type'].search([('name','ilike','Usuario final')],limit=1)
        return value and value.id or False
        
    partner_type_id = fields.Many2one(
        'res.partner.type', copy=False,
        default=_get_partner_type,
        string="Tipo de Cliente")
