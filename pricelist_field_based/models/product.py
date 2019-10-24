# coding: utf-8
from odoo import api, fields, models


class ProductPricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    base = fields.Selection(selection_add=[('field', 'Campo')])
    field_id = fields.Many2one('ir.model.fields', 'Campo')
    field_name = fields.Char(compute='_compute_field_name')

    @api.depends('field_id')
    def _compute_field_name(self):
        for record in self:
            if record.field_id:
                record.field_name = '%s -' % record.field_id.name
            else:
                record.field_name = ''


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    def price_compute(self, price_type, uom=False, currency=False, company=False):
        if price_type != 'field':
            return super(ProductProduct, self).price_compute(price_type, uom=uom, currency=currency, company=company)
        res = {}
        today = fields.Date.today()
        pricelist_item_obj = self.env['product.pricelist.item']
        for product in self:
            pricelist_item = pricelist_item_obj.search([
                '&', ('base', '=', 'field'),
                '&', '|', ('date_start', '=', False), ('date_start', '<=', today),
                '&', '|', ('date_end', '=', False), ('date_end', '>=', today),
                '|', ('applied_on', '=', '3_global'),
                '|', '&', ('applied_on', '=', '2_product_category'), ('categ_id', '=', product.categ_id.id),
                '|', '&', ('applied_on', '=', '1_product'), ('product_tmpl_id', '=', product.product_tmpl_id.id),
                '&', ('applied_on', '=', '0_product_variant'), ('product_id', '=', product.id)
            ], limit=1, order='pricelist_id')
            res.update(product.price_compute(pricelist_item.field_id.name, uom=uom, currency=currency, company=company))
        return res
