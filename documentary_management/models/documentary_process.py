# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError,ValidationError


class DProcessTag(models.Model):
    _name = 'dprocess.tag'
    _description = 'DArea Tags'

    active = fields.Boolean(default=True)
    color = fields.Integer(required=True, default=0)
    name = fields.Char(required=True)


class DocumentaryProcess(models.Model):
    _description = "Documentary Process"
    _name = 'documentary.process'
    _order = 'id desc'

    @api.model
    def _needaction_domain_get(self):
        return [('name', '!=', '')]

    name = fields.Char('Code', translate=True, default="New")
    desc = fields.Char('Name', translate=True, size=100)
    obs = fields.Text('Notes', translate=True)
    tag_ids = fields.Many2many('dprocess.tag', string='Tags')
    area_id = fields.Many2one('documentary.area', string='Area')

    image_medium = fields.Binary(
        "Medium-sized image",
        help="Product image")

    @api.one
    def _set_image_medium(self):
        self._set_image_value(self.image_medium)



    @api.model
    def create(self, vals):
        if vals.get('name', "New") == "New":
            vals['name'] = self.env['ir.sequence'].next_by_code('documentary.process') or "New"
        return super(DocumentaryProcess, self).create(vals)

    @api.multi
    def name_get(self):
        res = super(DocumentaryProcess, self).name_get()
        result = []
        for element in res:
            project_id = element[0]
            code = self.browse(project_id).name
            desc = self.browse(project_id).desc
            name = code and '[%s] %s' % (code, desc) or '%s' % desc
            result.append((project_id, name))
        return result