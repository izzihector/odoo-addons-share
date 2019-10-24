from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    same_currency_rate = fields.Boolean(compute='_compute_same_currency_rate')
    date_pricelist = fields.Date('Fecha tasa', states={'draft': [('readonly', False)]}, readonly=True)
    conversion_rate = fields.Float('Tasa de conversión', states={'draft': [('readonly', False)]}, readonly=True)
    last_pricelist_id = fields.Many2one('product.pricelist', 'Tarifa anterior')

    @api.onchange('date_pricelist', 'currency_id')
    def _onchange_pricelist(self):
        if self.currency_id and self.currency_id != self.env.user.company_id.currency_id:
            rate = self.env['res.currency.rate'].search([('currency_id', '=', self.currency_id.id),
                                                         ('name', '<=', self.date_pricelist or fields.Date.today())], limit=1, order='name desc')
            if rate:
                self.conversion_rate = rate.inv_rate
            else:
                self.conversion_rate = 1 / self.currency_id.rate
            if not self.date_pricelist:
                self.date_pricelist = rate.name or fields.Date.today()
            self.order_line.update({'original_currency_id': self.currency_id.id})
        else:
            self.conversion_rate = 1

    @api.depends('pricelist_id')
    def _compute_same_currency_rate(self):
        for record in self:
            record.same_currency_rate = self.currency_id == self.env.user.company_id.currency_id

    @api.multi
    def action_confirm(self):
        default_pricelist = self.env['product.pricelist'].search([('currency_id', '=', self.env.user.company_id.currency_id.id)], limit=1)
        for record in self:
            if record.conversion_rate != 1.0:
                record.note += '\nTasa de conversión de %s a %s: %.2f\nMonto original: %.2f' % (record.currency_id.name, default_pricelist.currency_id.name, record.conversion_rate, record.amount_total)
                record.last_pricelist_id = record.pricelist_id
                record.pricelist_id = default_pricelist
                for line in record.order_line:
                    line.currency_id = default_pricelist.currency_id
                    line.price_before_rate = line.price_unit
                    line.price_unit *= record.conversion_rate
        return super().action_confirm()

    def revert_rate(self):
        self.pricelist_id = self.last_pricelist_id
        for line in self.order_line:
            line.currency_id = self.pricelist_id.currency_id
            line.price_unit /= self.conversion_rate
        self.conversion_rate = 1


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    price_before_rate = fields.Monetary('Precio moneda original')
    original_currency_id = fields.Many2one('res.currency', 'Moneda original')
