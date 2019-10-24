##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api
import logging

class AccountInvoiceLine(models.Model):

    _inherit = "account.invoice.line"

    commission_amount = fields.Monetary(
        string = "Comisión",
        compute='_compute_commission_amount',
        currency_field='company_currency_id',
    )
    commission_tax = fields.Monetary(
        string = "Comisión Tax",
        compute='_compute_commission_amount',
        currency_field='company_currency_id',
    )
    
    @api.one
    def _compute_commission_amount(self):
        parameter = self.env['ir.config_parameter']
        commissioned_partner = parameter.sudo().get_param('sale_commission_report.commission_type')
        invoice = self.invoice_id
            
        for line in self:
            if not line.product_id.not_commission:
                percent_commission = line.product_id.commission #Producto
                if percent_commission == 0:
                    if not commissioned_partner or commissioned_partner == '0': #Cliente
                        partner = line.invoice_id.partner_id
                        percent_commission = partner.partner_type_id and partner.partner_type_id.commission or 0.6
                    
                    if commissioned_partner == '1': #Vendedor
                        vendor = line.invoice_id.user_id
                        percent_commission = vendor.commission > 0  and vendor.commission or 0.6
                subtotal = line.price_subtotal + self.get_global(invoice,line.price_subtotal) if invoice.global_amount > 0 else line.price_subtotal_signed
                line.commission_tax = percent_commission * (subtotal * 0.19) / 100.0 if line.invoice_line_tax_ids else 0.0
                line.commission_amount = percent_commission * subtotal / 100.0

    def get_global(self,invoice,afecto):
        untaxed = 0
        discount = (invoice.global_amount / 100.0) if invoice.global_type in ['percent'] else (invoice.global_amount * 100) / afecto
        
        if invoice.global_method == 'R':
            afecto = afecto
        
        if invoice.global_method == 'D' and invoice.global_type in ['amount']:
            afecto = afecto - discount
        
        #Asignacion de montos
        if invoice.global_type in ['amount'] and afecto > 0 and discount > 0:
            untaxed = untaxed - invoice.global_amount if self.global_method == 'D' else untaxed + invoice.global_amount

        if invoice.global_type in ['percent'] and afecto > 0 and discount > 0:
            amount_untaxed_global = (afecto * discount)
            untaxed = untaxed - amount_untaxed_global if invoice.global_method == 'D' else untaxed + amount_untaxed_global
        return untaxed
