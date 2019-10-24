# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError

class WizardMassiveLocked(models.TransientModel):
    _name = 'wizard.massive.locked'
    
    motive_locked = fields.Text(required=True, string="Motivo", size=128)

    def massives_locked(self):
        record_ids = self._context.get('active_ids')
        if not record_ids:
            raise UserError('No existen facturas seleccionadas.')
            
        for invoice in self.env['account.invoice'].browse(record_ids):
            partner_id  = invoice.partner_id
            vals = {'account_filter': 'bloqueado',
                    'motive_locked': self.motive_locked,}
            self.env['res.partner'].browse(partner_id.id).write(vals)