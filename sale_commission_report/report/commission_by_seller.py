# -*- coding: utf-8 -*-

import time
import decimal
from odoo.exceptions import UserError, RedirectWarning, ValidationError
from odoo import api, models, _
#from odoo.addons.report_xlsx import ReportXlsx
from .. import aid as a


class ReportCommisionbySellersPDF(models.AbstractModel):
    _name = 'report.sale_commission_report.commission_by_seller_pdf'

    def get_title(self, w, title=False):
        if title:
            if not w.all_sellers:
                if len(w.user_ids) == 1:
                    return _('COMISIÓN POR VENDEDORES: {}').format(
                        w.user_ids.name)
            return _('COMISIÓN POR VENDEDORES')
        return _('Desde {} hasta {}.').format(w.date_from.strftime('%d/%m/%Y'), w.date_to.strftime('%d/%m/%Y'))


    def set_dicc_total(self, dicc):
        list_data = []
        print (dicc)
        for k, v in dicc.items():
            print ('k::::',k)
            print ('V::::',v)
            #percent = v['salesman'].commission or 0.0
            vendor = v['salesman'].name or '*** Unknown ***'
            total = sum([i[2] for i in v['lines']])
            neto = sum([i[0] for i in v['lines']])
            iva = sum([i[1] for i in v['lines']])
            net_comm = sum([i[3] for i in v['lines']])
            total_comm = sum([i[4] for i in v['lines']])

            list_data.append((vendor, neto, iva, total, total_comm, net_comm ))

        return sorted(list_data, key=lambda element: (element[-1]), reverse=True)

    def get_data_total(self, invoices, orders):
        dicc = {}
        
        for i in invoices:
            if i.user_id.id not in dicc:
                dicc[i.user_id.id] = {'salesman': i.user_id, 'lines': []}

            dicc[i.user_id.id]['lines'].append((
                i.amount_untaxed * (-1 if i.sii_code == '61' and amount_untaxed > 0 else 1),
                i.amount_tax * (-1 if i.sii_code == '61' and amount_tax > 0 else 1),
                i.amount_total * (-1 if i.sii_code == '61' and amount_total > 0 else 1),
                i.commission_net * (-1 if i.sii_code == '61' and amount_total > 0 else 1),
                i.commission_total * (-1 if i.sii_code == '61' and amount_total > 0 else 1),
                ))

        for pos in orders:
            if pos.user_id.id not in dicc:
                dicc[pos.user_id.id] = {
                    'salesman': pos.user_id,
                    'lines': []}

            dicc[pos.user_id.id]['lines'].append((
                pos.amount_untaxed * (-1 if pos.sii_code == '61' and pos.amount_untaxed > 0 else 1),
                pos.amount_tax * (-1 if pos.sii_code == '61' and pos.amount_tax > 0 else 1),
                pos.amount_total * (-1 if pos.sii_code == '61' and pos.amount_total > 0 else 1)
            ))

        return self.set_dicc_total(dicc)

    def get_data(self, w):
        """Logica para obtener los datos del reporte."""
        invoice_domain = [
            ('date_invoice', '>=', w.date_from),
            ('date_invoice', '<=', w.date_to),
            ('type', 'in', ['out_invoice', 'out_refund'])]

        pos_order_domain = [
            ('invoice_id', '=', False),
            ('date_order', '>=', w.date_from.strftime("%Y-%m-%d") + ' 00:00:00'),
            ('date_order', '<=', w.date_to.strftime("%Y-%m-%d") + ' 23:59:59')]

        if not w.all_sellers:
            invoice_domain.append(('user_id', 'in', w.user_ids.ids))
            pos_order_domain.append(('user_id', 'in', w.user_ids.ids))

        if w.state == 'all':
            invoice_domain.append(('state', 'in', ['paid', 'open']))
            pos_order_domain.append(('state', 'in', ['paid', 'done', 'invoiced']))
        else:
            invoice_domain.append(('state', '=', w.state))
            pos_order_domain.append(('state', '=', w.state))

        invoices = self.env['account.invoice'].search(invoice_domain)
        pos_order_domain.append(('invoice_id', 'not in', invoices.ids))
        orders = self.env['pos.order'].search(pos_order_domain)
        list_data = []

        if not invoices and not orders:
            return list_data

        if w.type_report == 'total':
            list_data = self.get_data_total(invoices, orders)
        
        print ('list_data:::',list_data)
        #list_data::: [('Administrator', 2619496.0, 497704.0, 3117200.0, 155860.0, 5.0, 130974.8)]
        return list_data


    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get('form'):
            raise UserError(_("Form content is missing, this report cannot be printed."))
        
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_ids', []))
        list_data = self.get_data(docs)
        
        return {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],#data,
            'docs': docs,
            'time': time,
            'title': self.get_title(docs, True),
            'subtitle': self.get_title(docs),
            'list_data': list_data,
            'order_commission': a.order_commission,
            'amount_untax': sum([i[1] for i in list_data]),
            'amount_tax': sum([i[2] for i in list_data]),
            'amount_total': sum([i[3] for i in list_data]),
            'amount_comission': sum([i[4] for i in list_data]),
            'amount_comission_neta': sum([i[-1] for i in list_data]),
        }

# ~ class ReportCommisionbySellersXLSX(ReportXlsx):
    # ~ """."""

    # ~ def generate_xlsx_report(self, workbook, data, wizard):
        # ~ """."""
        # ~ sheet = workbook.add_worksheet('Report')
        # ~ pdf = self.env[
            # ~ 'report.sale_commission_report.commission_by_seller_pdf']

        # ~ list_data = pdf.get_data(wizard)
        # ~ format_title = workbook.add_format(a.format_title)
        # ~ format_subtitle = workbook.add_format(a.format_subtitle)
        # ~ format_title.set_align('center')
        # ~ format_subtitle.set_align('center')
        # ~ bold = workbook.add_format({'bold': True})

        # ~ c = 4
        # ~ sheet.merge_range("A1:G1", pdf.get_title(wizard, True), format_title)
        # ~ sheet.merge_range("A2:G2", pdf.get_title(wizard), format_subtitle)
        # ~ sheet.write('A' + str(c), _('Seller'), bold)
        # ~ sheet.write('B' + str(c), _('Porcentaje'), bold)
        # ~ sheet.write('C' + str(c), _('Monto neto'), bold)
        # ~ sheet.write('D' + str(c), _('Comisión neta'), bold)
        # ~ sheet.write('E' + str(c), _('IVA'), bold)
        # ~ sheet.write('F' + str(c), _('Monto total'), bold)
        # ~ sheet.write('G' + str(c), _('Comisión total'), bold)

        # ~ for value in list_data:
            # ~ sheet.write(c, 0, value[0])
            # ~ sheet.write(c, 1, value[-2])
            # ~ sheet.write(c, 2, value[1])
            # ~ sheet.write(c, 3, value[-1])
            # ~ sheet.write(c, 4, value[2])
            # ~ sheet.write(c, 5, value[3])
            # ~ sheet.write(c, 6, value[4])
            # ~ c += 1

        # ~ sheet.write(c, 2, sum([i[1] for i in list_data]), bold)
        # ~ sheet.write(c, 3, sum([i[-1] for i in list_data]), bold)
        # ~ sheet.write(c, 4, sum([i[2] for i in list_data]), bold)
        # ~ sheet.write(c, 5, sum([i[3] for i in list_data]), bold)
        # ~ sheet.write(c, 6, sum([i[4] for i in list_data]), bold)


# ~ ReportCommisionbySellersXLSX(
    # ~ 'report.sale_commission_report.report_commission_by_seller.xlsx',
    # ~ 'wizard.commission.by.seller.report')
