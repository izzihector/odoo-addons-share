# -*- coding: utf-8 -*-

from odoo import api, models
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    """."""

    _inherit = 'purchase.order'

    @api.multi
    def action_view_invoice(self):
        """."""
        if self.company_id.purchase_validate_pickings and not self.picking_ids:
            raise ValidationError(
                'No es posible crear facturas debido a que no '
                'existe al menos una guía de despacho asociada')
        if self.company_id.purchase_validate_pickings and \
                not any(picking.state == 'done'
                        for picking in self.picking_ids):
            raise ValidationError(
                'No es posible crear facturas debido a que no existe '
                'al menos una guía de despacho asociada en estatus Hecho')
        return super().action_view_invoice()
