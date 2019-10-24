# coding: utf-8
from odoo import _, api, models
from odoo.exceptions import AccessError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def unlink(self):
        for record in self:
            if record.customer and not self.env.user.can_delete_customers:
                raise AccessError(_(u'You cannot delete customers'))
            elif record.supplier and not self.env.user.can_delete_suppliers:
                raise AccessError(_(u'You cannot delete suppliers'))
        return super(ResPartner, self).unlink()
