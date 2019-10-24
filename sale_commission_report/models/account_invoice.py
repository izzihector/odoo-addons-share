##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api
import logging


class AccountInvoice(models.Model):

    _inherit = "account.invoice"

    commission_net = fields.Monetary(
        string = "Comisión Neta",
        compute='_compute_commission_amount',
        currency_field='company_currency_id',
    )
    commission_total = fields.Monetary(
        string = "Comisión Total",
        compute='_compute_commission_amount',
        currency_field='company_currency_id',
    )

    @api.depends('invoice_line_ids.commission_amount')
    def _compute_commission_amount(self):
        for invoice in self:
            commission_net = commission_tot = 0
            if invoice.type in ['out_invoice','out_refunf']:
                sign = invoice.sii_code == '61' and -1 or 1
                commission_net = sum(invoice.mapped('invoice_line_ids.commission_amount')) * sign
                commission_tot = sum(invoice.mapped('invoice_line_ids.commission_tax')) * sign
            invoice.commission_net = commission_net
            invoice.commission_total = commission_tot + commission_net
