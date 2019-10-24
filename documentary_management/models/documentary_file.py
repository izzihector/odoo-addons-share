# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError,ValidationError


class DFileTag(models.Model):
    _name = 'dfile.tag'
    _description = 'DArea Tags'

    active = fields.Boolean(default=True)
    color = fields.Integer(required=True, default=0)
    name = fields.Char(required=True)


class DocumentaryFile(models.Model):
    _description = "Documentary File"
    _name = 'documentary.file'
    _order = 'id desc'

    @api.model
    def _needaction_domain_get(self):
        return [('name', '!=', '')]

    name = fields.Char('Code', translate=True, default="New")
    desc = fields.Char('Name', translate=True, size=100)
    obs = fields.Text('Notes', translate=True)
    tag_ids = fields.Many2many('darea.tag', string='Tags')
    process_id = fields.Many2one('documentary.process', string='Process')
    partner_id = fields.Many2one('res.partner', string='Partner')

    user_id = fields.Many2one('res.users', string='Responsable', track_visibility='onchange',
                              default=lambda self: self.env.user)

    file_name = fields.Char("File")
    file_01 = fields.Binary(
        string='File',
        copy=False,
        help='File')

    image_medium = fields.Binary(
        "Medium-sized image",
        help="Product image")

    @api.one
    def _set_image_medium(self):
        self._set_image_value(self.image_medium)



    @api.model
    def create(self, vals):
        if vals.get('name', "New") == "New":
            vals['name'] = self.env['ir.sequence'].next_by_code('documentary.file') or "New"
        return super(DocumentaryFile, self).create(vals)

    @api.multi
    def name_get(self):
        res = super(DocumentaryFile, self).name_get()
        result = []
        for element in res:
            project_id = element[0]
            code = self.browse(project_id).name
            desc = self.browse(project_id).desc
            name = code and '[%s] %s' % (code, desc) or '%s' % desc
            result.append((project_id, name))
        return result