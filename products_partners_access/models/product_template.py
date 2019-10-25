# coding: utf-8
from lxml import etree

from odoo import api, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(ProductTemplate, self).fields_view_get(view_id=view_id,
                                                           view_type=view_type,
                                                           toolbar=toolbar,
                                                           submenu=submenu)
        if view_type == 'form' and not self.env.user.product_access:
            doc = etree.XML(res['arch'])
            for node in doc.xpath('//form'):
                node.set('create', 'false')
                node.set('edit', 'false')
            res['arch'] = etree.tostring(doc)
        elif view_type == 'tree' and not self.env.user.product_access:
            doc = etree.XML(res['arch'])
            for node in doc.xpath('//tree'):
                node.set('create', 'false')
            res['arch'] = etree.tostring(doc)
        elif view_type == 'kanban' and not self.env.user.product_access:
            doc = etree.XML(res['arch'])
            for node in doc.xpath('//kanban'):
                node.set('create', 'false')
            res['arch'] = etree.tostring(doc)
        return res


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(ProductProduct, self).fields_view_get(view_id=view_id,
                                                          view_type=view_type,
                                                          toolbar=toolbar,
                                                          submenu=submenu)
        if view_type == 'form' and not self.env.user.product_access:
            doc = etree.XML(res['arch'])
            for node in doc.xpath('//form'):
                node.set('create', 'false')
                node.set('edit', 'false')
            res['arch'] = etree.tostring(doc)
        elif view_type == 'tree' and not self.env.user.product_access:
            doc = etree.XML(res['arch'])
            for node in doc.xpath('//tree'):
                node.set('create', 'false')
            res['arch'] = etree.tostring(doc)
        elif view_type == 'kanban' and not self.env.user.product_access:
            doc = etree.XML(res['arch'])
            for node in doc.xpath('//kanban'):
                node.set('create', 'false')
            res['arch'] = etree.tostring(doc)
        return res
