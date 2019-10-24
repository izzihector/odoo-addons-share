# -*- coding: utf-8 -*-
import time
import xlwt
import base64
import re
import io
import calendar
from io import StringIO
from datetime import datetime
from odoo import fields, models, api, _
from .. import aid as a


class WizardReportCustomer(models.TransientModel):
    """Wizard commission.by.seller."""

    _name = 'wizard.commission.by.seller.report'
    _description = 'Commission by seller'

    all_sellers = fields.Boolean(
        'Todos', default=True, help="Select all sellers")

    user_ids = fields.Many2many(
        'res.users', 'res_commission_users_rel', 'c_id', 'user_id',
        string='Vendedores')

    date_from = fields.Date(
        string='Date from', required=True, default=fields.Date.today())

    date_to = fields.Date(
        string='Date to', required=True, default=fields.Date.today())

    type_report = fields.Selection(
        [
            ('total', 'Resumido'),
            # ('product', 'Products'),
            # ('category', 'Categories')
        ], string='Tipo de reporte', default='total')

    state = fields.Selection(
        [('all', 'Abiertas, pagadas y publicadas'), ('open', 'Abiertas'),
         ('paid', 'Pagadas'), ('done', 'Publicadas')],
        string='Estado', default='all')


    @api.multi
    def print_pdf(self):
        """Generate PDF report."""
        self.ensure_one()
        a.valid_date(self.date_from, self.date_to)
        data = {}
        used_context = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read([])[0]
        data['form']['used_context'] = dict(used_context, lang=self.env.context.get('lang', 'es_CL'))
        return self._print_report(data)


    def _print_report(self, data):
        return self.env.ref('sale_commission_report.sale_report_commission_seller').with_context(landscape=True).report_action(self, data=data)


    def print_xlsx(self, data):
        """Generate XLSX report."""
        a.valid_date(self.date_from, self.date_to)
        workbook = xlwt.Workbook(encoding="utf-8")
        worksheet = workbook.add_sheet('Report')
        pdf = self.env['report.sale_commission_report.commission_by_seller_pdf']
        wizard = self
        today = datetime.today().strftime("%d-%m-%Y")
        list_data = pdf.get_data(wizard)
        #format_title = workbook.add_format(a.format_title)
        #format_subtitle = workbook.add_format(a.format_subtitle)
        #format_title.set_align('center')
        #format_subtitle.set_align('center')
        #bold = workbook.add_format({'bold': True})
        style_title = xlwt.easyxf("font:height 200; font: name Liberation Sans, bold on,color black; align: horiz center")
        style_table_header = xlwt.easyxf("font:height 200; font: name Liberation Sans, bold on,color black; align: horiz center")
        header_style1 = xlwt.easyxf('font: bold on, height 160; align: wrap on, horiz center, vert center;')
        header_style2 = xlwt.easyxf('pattern: pattern solid, pattern_fore_colour pale_blue, pattern_back_colour pale_blue; font: bold on, height 160; align: wrap on, horiz center, vert center;')
        header_style3 = xlwt.easyxf('pattern: pattern solid, pattern_fore_colour gray25, pattern_back_colour gray25; font: bold on, height 160; align: wrap on, horiz center, vert center;')
        title_style = xlwt.easyxf('font: bold on, height 160; align: wrap on, horiz center, vert center; border: top thick, right thick, bottom thick, left thick;')
        base_style = xlwt.easyxf('font: height 140; align: wrap on, horiz center')
        base_style_left = xlwt.easyxf('font: height 140; align: wrap on, horiz left')
        base_style_right = xlwt.easyxf('font: height 140; align: wrap on, horiz right')
        base_style_right2 = xlwt.easyxf('font: height 140, bold on; align: wrap on, horiz right; border: top thick;')
        decimal_style = xlwt.easyxf('font: height 140; align: wrap yes, horiz right',num_format_str='$#,##0')
        decimal_style2 = xlwt.easyxf('font: height 140, bold on; align: wrap yes, horiz right; border: top thick;',num_format_str='$#,##0')
        date_style = xlwt.easyxf('font: height 140; align: wrap yes; font: bold on; align: wrap on, horiz center, vert center;', num_format_str='DD-MM-YYYY')
        date_style_title = xlwt.easyxf('font: bold on, height 160; align: wrap yes; font: bold on; align: wrap on, horiz center, vert center;', num_format_str='DD-MM-YYYY')
        datetime_style = xlwt.easyxf('font: height 140; align: wrap yes', num_format_str='YYYY-MM-DD HH:mm:SS')

        row_index = 3
        worksheet.write_merge(0, 2, 0, 6,pdf.get_title(wizard, True), header_style1)
        worksheet.write(row_index, 1, 'Vendedor', header_style3)
        #worksheet.write(row_index, 2, 'Porcentaje', header_style3)
        worksheet.write(row_index, 2, 'Monto neto', header_style3)
        worksheet.write(row_index, 3, 'Comisión neta', header_style3)
        worksheet.write(row_index, 4, 'IVA', header_style3)
        worksheet.write(row_index, 5, 'Monto total', header_style3)
        worksheet.write(row_index, 6, 'Comisión total', header_style3)
        row_index+=1
        
        for value in list_data:
            worksheet.write(row_index, 1, re.sub("\r", " ", value[0]), base_style_left)
            #worksheet.write(row_index, 2, float(re.sub("\r", " ", str(value[-2]).replace(".0",""))), base_style_left)
            worksheet.write(row_index, 2, float(re.sub("\r", " ", str(value[1]).replace(".0",""))), decimal_style)
            worksheet.write(row_index, 3, float(re.sub("\r", " ", str(value[-1]).replace(".0",""))), decimal_style)
            worksheet.write(row_index, 4, float(re.sub("\r", " ", str(value[2]).replace(".0",""))), decimal_style)
            worksheet.write(row_index, 5, float(re.sub("\r", " ", str(value[3]).replace(".0",""))), decimal_style)
            worksheet.write(row_index, 6, float(re.sub("\r", " ", str(value[4]).replace(".0",""))), decimal_style)
            row_index+=1
        
        row_index+=1
        worksheet.write(row_index, 0, 'TOTALES', header_style3)
        worksheet.write(row_index, 2, float(re.sub("\r", " ", str(sum([i[1] for i in list_data])).replace(".0",""))) , decimal_style2)
        worksheet.write(row_index, 3, float(re.sub("\r", " ", str(sum([i[-1] for i in list_data])).replace(".0",""))), decimal_style2)
        worksheet.write(row_index, 4, float(re.sub("\r", " ", str(sum([i[2] for i in list_data])).replace(".0",""))) ,decimal_style2)
        worksheet.write(row_index, 5, float(re.sub("\r", " ", str(sum([i[3] for i in list_data])).replace(".0",""))) , decimal_style2)
        worksheet.write(row_index, 6, float(re.sub("\r", " ", str(sum([i[4] for i in list_data])).replace(".0",""))) , decimal_style2)
        worksheet.col(1).width = 12000
        
        fp = io.BytesIO()
        workbook.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        data_b64 = base64.encodestring(data)
        attach = self.env['ir.attachment'].create({
            'name': '%s %s.xls'%('Comision',today),
            'type': 'binary',
            'datas': data_b64,
            'datas_fname': '%s %s.xls'%('Comision',today),
        })
        return {
                'type' : "ir.actions.act_url",
                'url': "web/content/?model=ir.attachment&id="+str(attach.id)+"&filename_field=datas_fname&field=datas&download=true&filename="+str(attach.name),
                'target': "self",
                'no_destroy': False,
        }
