# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _

class TaxProductTemplate(models.Model):
    _inherit = "product.template"

    @api.multi
    @api.onchange('available_in_pos')
    def _available_pos_tax(self):
        if self.available_in_pos:
            if self.env.user.company_id.taxes_id:
                self.taxes_id = self.env.user.company_id.taxes_id
