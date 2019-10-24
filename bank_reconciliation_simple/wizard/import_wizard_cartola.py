#-*- coding: utf-8 -*-

import os
import base64
import logging
import tempfile
import unicodedata as ud

from datetime import datetime

from odoo import api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

try:
    import csv
except ImportError:
    _logger.debug('Cannot `import csv`.')

try:
    import xlrd
except ImportError:
    _logger.debug('Cannot `import xlrd`.')


class ImportWizardCartola(models.TransientModel):
    """Ventana para importar Cartola."""

    _name = 'import.wizard.cartola'
    _description = "Ventana para importar Cartola"

    HEADER = [
        'voucher', 'date', 'description', 'no_doc', 'cargo', 'abono']

    file = fields.Binary('Archivo (csv o xlsx)')
    file_name = fields.Char('Nombre del Archivo')
    bank_id = fields.Many2one('res.bank', 'Banco', required=True)

    @api.model
    def csv_validator(self, xml_name):
        """."""
        name, extension = os.path.splitext(xml_name)
        return (True, extension) if extension in ['.csv', '.xlsx'] else False

    def verificar_date(self, date, count, workbook=False):
        """."""
        if isinstance(date, (str,)):
            format_list = [
                '%Y-%m-%d', '%d-%m-%Y', '%m-%d-%Y',
                '%Y/%m/%d', '%d/%m/%Y', '%m/%d/%Y']
            date = date.strip()
            for formato in format_list:
                try:
                    date = datetime.strptime(date, formato)
                    return date.strftime('%Y-%m-%d')
                except:
                    pass

        else:
            date = xlrd.xldate.xldate_as_datetime(
                date, workbook.datemode)
            return date.strftime('%Y-%m-%d')

        raise UserError(
            "Error en el formato de la fecha (date).\nLinea {} del archivo".format(count))

    def verificar_description(self, description, count, workbook=False):
        """."""
        return ud.normalize('NFC', str(description))

    def verificar_voucher(self, voucher, count, workbook=False):
        """."""
        try:
            return float(voucher)
        except:
            raise UserError(
                "Error en el formato del voucher se esperaba un número.\nLinea {} del archivo".format(count))

    def verificar_no_doc(self, no_doc, count, workbook=False):
        """."""
        if not isinstance(no_doc, (str,)):
            no_doc = str(int(no_doc))
        return no_doc if no_doc else ''

    def verificar_cargo_abono(self, amount, count, workbook=False):
        """."""
        if isinstance(amount, (str,)):
            amount = amount.strip().replace('-', '0.0') or '0.0'
        amount = float(amount)
        if type(amount) != float:
            raise UserError(
                "Error en el formato del cargo/abono se esperaba un número.\nLinea {} del archivo".format(count))
        return amount

    @api.multi
    def import_csv(self):
        """."""
        ext = self.csv_validator(self.file_name)
        if not ext:
            raise UserError(
                "El archivo debe ser de extensión (.csv o .xlsx)")

        path = tempfile.gettempdir() + '/template' + ext[-1]
        f = open(path, 'wb')
        f.write(base64.b64decode(self.file))
        f.close()

        active_id = self._context.get('active_id')
        obj_model = self.env['bank.reconciliation.simple']
        validate_header = False

        data = []
        if ext[-1] == '.csv':
            for count, i in enumerate(
                    [line for line in csv.DictReader(open(path))], 2):

                val = dict(i)
                if not validate_header:
                    if sorted(list(i.keys())) != sorted(self.HEADER):
                        break
                val['date'] = self.verificar_date(
                    val['date'], count)
                val['voucher'] = self.verificar_voucher(
                    val['voucher'], count)

                val['description'] = self.verificar_description(
                    val['description'], count)
                val['no_doc'] = self.verificar_no_doc(
                    val['no_doc'], count)
                val['cargo'] = self.verificar_cargo_abono(
                    val['cargo'], count)
                val['abono'] = self.verificar_cargo_abono(
                    val['abono'], count)
                val.update(
                    {'bank_id': self.bank_id.id,
                     'reconciliation_id': active_id})
                data.append(val)
                validate_header = True
        else:
            workbook = xlrd.open_workbook(path)
            worksheet = workbook.sheet_by_index(0)
            first_row = []
            for col in range(worksheet.ncols):
                first_row.append(worksheet.cell_value(0, col))
            if not validate_header:
                if sorted(first_row) == sorted(self.HEADER):
                    validate_header = True
            if validate_header:
                for count, row in enumerate(range(1, worksheet.nrows), 2):
                    val = {}
                    for col in range(worksheet.ncols):
                        val[first_row[col]] = worksheet.cell_value(row, col)
                    val['date'] = self.verificar_date(
                        val['date'], count, workbook)
                    val['voucher'] = self.verificar_voucher(
                        val['voucher'], count, workbook)
                    val['description'] = self.verificar_description(
                        val['description'], count, workbook)
                    val['no_doc'] = self.verificar_no_doc(
                        val['no_doc'], count, workbook)
                    val['cargo'] = self.verificar_cargo_abono(
                        val['cargo'], count, workbook)
                    val['abono'] = self.verificar_cargo_abono(
                        val['abono'], count, workbook)
                    val.update(
                        {'bank_id': self.bank_id.id,
                         'reconciliation_id': active_id})
                    data.append(val)

        if not validate_header:
            raise UserError(
                "La cabecera del archivo debe estar "
                "compuesta por: \n {}".format(', '.join(self.HEADER)))
        for values in data:
            obj_model.create(values)
        del path
