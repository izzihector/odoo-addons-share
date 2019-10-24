# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import pytz
from odoo import models, fields, api

class SchedulerLocked(models.Model):
    _name = 'scheduler.customer.locked'

    def processAutomatic(self):
        def time_now(formato='%Y-%m-%d'):
            tz = pytz.timezone('America/Santiago')
            return datetime.now(tz).strftime(formato)
        company_id = self.env['res.company']._company_default_get('scheduler.customer.locked')
        invoices = self.env['account.invoice'].search([('type','=','out_invoice')])
        today = datetime.strptime(time_now(), '%Y-%m-%d')
        for invoice in invoices:
            if invoice.state != 'paid':
                if invoice.date_due:
                    days = datetime.strptime(invoice.date_due, '%Y-%m-%d') - today
                    invoice.number_days = days.days
                else:
                    invoice.number_days = 0
                total_days = invoice.number_days + company_id.days
                if total_days < 0:
                    partner_id  = invoice.partner_id
                    vals = {'account_filter': 'bloqueado','motive_locked': 'Bloqueo automatico.',}
                    self.env['res.partner'].browse(partner_id.id).write(vals)