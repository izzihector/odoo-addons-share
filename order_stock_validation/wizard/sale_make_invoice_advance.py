# -*- coding: utf-8 -*-

from odoo import api, models
from odoo.exceptions import ValidationError


class SaleAdvancePaymentInv(models.TransientModel):
    """."""

    _inherit = "sale.advance.payment.inv"

    @api.multi
    def create_invoices(self):
        """."""
        sales = self.env['sale.order'].browse(
            self._context.get('active_ids', []))

        for sale in sales:

            if sale.company_id.sale_validate_pickings and not sale.picking_ids:

                raise ValidationError(
                    'No es posible crear facturas debido a que no existe'
                    ' al menos un albarán asociado')

            if sale.company_id.sale_validate_pickings and \
                    not any(picking.state == 'done'
                            for picking in sale.picking_ids):

                raise ValidationError(
                    'No es posible crear facturas debido a que no existe'
                    ' al menos un albarán asociado en estatus Hecho')

        return super().create_invoices()
