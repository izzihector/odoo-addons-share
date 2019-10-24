# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO, Open Source Management Solution
#    Copyright (C) 2016 Steigend IT Solutions
#    For more details, check COPYRIGHT and LICENSE files
#
##############################################################################
{
    'name': "Cuentas Analíticas de Usuario por defecto",
    'summary': """Carga Cuentas Analíticas de Usuario por defecto al crear un Producto o Factura""",
    'description': """
        Carga Cuentas Analíticas de Usuario por defecto al crear un Producto o Factura.
    """,
    'author': "Falcón Solutions",
    'maintainer': 'Falcon Solutions',
    'website': 'http://www.falconsolutions.cl',
    'license': 'AGPL-3',
    'category': 'Account',
    'version': '10.0.1',
    'depends': ['analytic',
                'sale',
                'purchase',
                'account',
                ],
    'data': [
        'views/res_user_view.xml',
    ],
    'demo': [
    ],
}
