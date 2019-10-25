# coding: utf-8
from lxml import etree

from odoo import api, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(ResPartner, self).fields_view_get(view_id=view_id,
                                                      view_type=view_type,
                                                      toolbar=toolbar,
                                                      submenu=submenu)
        if not self.env.user.partner_access:
            if view_type == 'form':
                doc = etree.XML(res['arch'])
                for node in doc.xpath('//form'):
                    node.set('create', 'false')
                    node.set('edit', 'false')
                res['arch'] = etree.tostring(doc)
            elif view_type == 'tree':
                doc = etree.XML(res['arch'])
                for node in doc.xpath('//tree'):
                    node.set('create', 'false')
                res['arch'] = etree.tostring(doc)
            elif view_type == 'kanban':
                doc = etree.XML(res['arch'])
                for node in doc.xpath('//kanban'):
                    node.set('create', 'false')
                res['arch'] = etree.tostring(doc)
        return res
