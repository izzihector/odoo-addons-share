# -*- coding: utf-8 -*-

import re
import os
import base64
import random
import tempfile
import unicodedata

from odoo import api, models


class ProductPricelist(models.Model):
    """."""

    _inherit = "product.pricelist"

    def clean_accents(self, text):
        """."""
        string = ''.join((c for c in unicodedata.normalize(
            'NFD', text) if unicodedata.category(c) != 'Mn'))
        return re.sub(r'[^a-zA-Z0-9- :/.]', '', string)

    @api.multi
    def export_pricelist(self):
        """."""
        # res = {}
        # fname = '%s_previred.csv' % self.name
        # path = '{}/{}'.format(tempfile.gettempdir(), fname)
        # file = open(path, 'w')

        res = {}
        fname = '{}_lista_precios_{}.csv'.format(
            self.name, str(random.randint(1000, 9000)))
        path = '{}/{}'.format(tempfile.gettempdir(), fname)

        file = open(path, 'w', encoding='utf-8')

        file.write('code, name, price, coste' + os.linesep)

        id_tarifa = self.id

        obj_product_pricelist_item = self.env['product.pricelist.item'].search(
            [('pricelist_id', '=', id_tarifa)])

        for id in obj_product_pricelist_item:

            code = ""

            value_c = 0
            if id.applied_on == '1_product':
                if id.product_tmpl_id.default_code:
                    code = id.product_tmpl_id.default_code
                    nombre = id.product_tmpl_id.name
                    value_c = str(
                        id.product_tmpl_id.standard_price).replace(".0", "")

            if id.applied_on == '0_product_variant':
                if id.product_id.default_code:
                    code = id.product_id.default_code
                    nombre = id.product_id.name

            value_p = id.fixed_price
            if (value_p % 1) == 0 or value_p.is_integer():
                value_p = int(value_p)

            if not code == '':
                file.write(u'%s,%s,%s,%s\n' % (code, nombre.replace(
                    ",", ".").replace(";", "."), value_p, value_c))

        file.close()

        data = base64.b64encode(open(path, 'r').read().encode('utf-8'))

        attach_vals = {'name': fname, 'datas': data, 'datas_fname': fname}

        doc_id = self.env['ir.attachment'].create(attach_vals)

        res['type'] = 'ir.actions.act_url'

        res['target'] = 'new'

        res['url'] = "web/content/?model=ir.attachment&id=" + str(
            doc_id.id) + "&filename_field=datas_fname&field=datas&download=true&filename=" + str(self.clean_accents(doc_id.name))

        return res
