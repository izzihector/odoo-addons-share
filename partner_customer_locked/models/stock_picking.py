# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class Picking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def create(self, vals):
        data = self.env['res.partner'].search([('id','=',vals['partner_id'])])
        if data.account_filter == 'bloqueado':
            raise UserError('{0} se encuentra bloqueado!'.format(data.name.encode('utf-8').strip()))
        return super(Picking, self).create(vals)

    @api.multi
    def write(self, vals):
        if 'partner_id' in vals:
            data = self.env['res.partner'].search([('id','=',vals['partner_id'])])
            if data.account_filter == 'bloqueado':
                raise UserError('{0} se encuentra bloqueado!'.format(data.name.encode('utf-8').strip()))
        return super(Picking, self).write(vals)
    
    @api.multi
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        res={}
        if self.partner_id.account_filter == 'bloqueado':
            partner_name = self.partner_id.name.encode('utf-8').strip()
            warning = {
                'title': ("Aviso"),
                'message': '{0} se encuentra (bloqueado)'.format(partner_name)
                }
            res['warning'] = warning
            self.partner_id = False
            return res