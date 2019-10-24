# -*- coding: utf-8 -*-

import base64

from odoo import fields, models, modules


class DownloadTemplateCartola(models.TransientModel):
    """Descargar plantilla para importar cartola."""

    _name = 'download.template.cartola'
    _description = 'Descargar plantilla para importar cartola'

    def _get_template_csv(self):
        """."""
        template = open(modules.get_module_resource(
            'bank_reconciliation_simple', 'templates',
            'template_base.csv')).read()
        return base64.b64encode(template.encode('utf-8').strip())

    def _get_template_xlsx(self):
        """."""
        template = open(modules.get_module_resource(
            'bank_reconciliation_simple', 'templates',
            'template_base.xlsx'), 'rb').read()
        return base64.b64encode(template)

    template = fields.Binary('Template', default=_get_template_csv)
    template_xlsx = fields.Binary('Template', default=_get_template_xlsx)

    ext = fields.Selection([
        ('csv', 'CSV'), ('xlsx', 'Excel')], string='Formato', default='csv')

    def download_template(self):
        """."""
        url = '/web/bank_reconciliation_simple?model=download.template.cartola'
        url += '&id={}&filename=plantilla_base.{}'.format(self.id, self.ext)
        return {'type': 'ir.actions.act_url', 'url': url, 'target': 'new'}
