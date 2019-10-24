# -*- coding: utf-8 -*-

import base64

from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import (
    serialize_exception, content_disposition)


class DownloadTemplate(http.Controller):
    """."""

    @http.route(
        '/web/bank_reconciliation_simple', type='http', auth="public")
    @serialize_exception
    def download_template(self, model, id, filename=None, **kw):
        """."""
        model = http.request.env[model].search([('id', '=', id)])
        filecontent = False
        name = 'plantilla_base.xlsx'

        if model.ext == 'csv':
            filecontent = base64.b64decode(model.template or '')
            name = 'plantilla_base.csv'
        else:
            filecontent = base64.b64decode(model.template_xlsx or '')

        if not filecontent:
            return request.not_found()

        return request.make_response(
            filecontent,
            [('Content-Type', 'application/octet-stream'),
                ('Content-Disposition', content_disposition(name))])
