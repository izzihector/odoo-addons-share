# coding: utf-8
from odoo import api, fields, models


class ProductTag(models.Model):
    _name = 'product.tag'
    _description = 'Product Tags'

    active = fields.Boolean(default=True)
    color = fields.Integer(required=True, default=0)
    name = fields.Char(required=True)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    tag_ids = fields.Many2many('product.tag', string='Tags')

    @api.model
    def create(self, vals):
        template = super(ProductTemplate, self).create(vals)
        if 'tag_ids' in vals:
            for variant in template.product_variant_ids:
                variant.tag_ids = vals['tag_ids']
        return template

    @api.multi
    def write(self, vals):
        res = super(ProductTemplate, self).write(vals)
        if 'tag_ids' in vals:
            self.mapped('product_variant_ids').filtered(lambda v: not v.tag_ids).write({
                'tag_ids': vals['tag_ids']
            })
        return res


class ProductProduct(models.Model):
    _inherit = 'product.product'

    tag_ids = fields.Many2many('product.tag', string='Tags')
