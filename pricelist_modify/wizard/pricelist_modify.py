#-*- coding: utf-8 -*-

import os
import base64
import logging
import tempfile

from odoo import api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

try:
    import csv
except ImportError:
    _logger.debug('Cannot `import csv`.')


class PriceListModify(models.TransientModel):
    """."""

    _name = 'pricelist.modify'
    _description = "Modifica lista de precios"

    HEADER = ['codigo', 'precio']

    file = fields.Binary('Archivo .csv')
    file_name = fields.Char('Nombre del Archivo')

    @api.model
    def csv_validator(self, xml_name):
        """."""
        name, extension = os.path.splitext(xml_name)
        return True if extension == '.csv' else False

    @api.multi
    def import_csv(self):
        """."""
        if not self.csv_validator(self.file_name):
            raise UserError("El archivo debe ser de extension .csv")

        path = tempfile.gettempdir() + '/file.csv'

        f = open(path, 'wb')
        f.write(base64.b64decode(self.file))
        f.close()

        tarifa = self.env['product.pricelist'].browse(
            self._context.get('active_id'))

        items = tarifa.item_ids.filtered(
            lambda r: r.applied_on in ['1_product', '0_product_variant'])

        validate_header = False

        for i in [line for line in csv.DictReader(open(path))]:

            val = dict(i)

            if not validate_header:
                if list(i.keys()) != self.HEADER:
                    raise UserError(
                        "La cabecera del archivo debe estar compuesta por: \n"
                        "codigo, precio")

            for item in items:

                if item.applied_on == '1_product':
                    if item.product_tmpl_id.default_code == val['codigo']:
                        item.fixed_price = float(val['precio'])
                else:
                    if item.product_id.default_code == val['codigo']:
                        item.fixed_price = float(val['precio'])

            validate_header = True

        del path
