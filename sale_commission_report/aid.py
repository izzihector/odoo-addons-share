# -*- coding: utf-8 -*-

import pytz
import decimal

from odoo import _
from odoo.exceptions import UserError
from datetime import datetime

tz = pytz.timezone('America/Santiago')
decimal.getcontext().rounding = decimal.ROUND_DOWN

format_title = {
    'font_size': 14,
    'bottom': True,
    'right': True,
    'left': True,
    'top': True,
    'align': 'vcenter',
    'bold': True}

format_subtitle = {
    'font_size': 10,
    'bottom': True,
    'right': True,
    'left': True,
    'top': True,
    'align': 'vcenter',
    'bold': False}

trans = {
    'category': _('Categorias'),
    'product': _('Productos'),
    'all': _('Abiertas, pagadas y publicadas'),
    'paid': _('Pagadas'),
    'open': _('Abiertas'),
    'done': _('publicadas'),
    'total': _('Resumido'),
}

ranking_limit = 10


def get_year():
    """."""
    return int(datetime.now(tz).year)


def set_format_date(date, format_date='%Y-%m-%d'):
    """."""
    if isinstance(date, datetime):
        return date.strftime(format_date)
    # ~ if isinstance(date, datetime.date):
        # ~ return date.strftime(format_date)

    # ~ if isinstance(date, datetime):
        # ~ return datetime.strptime(
            # ~ date, '%Y-%m-%d %H:%M:%S').strftime(format_date)
    return datetime.strptime(date, '%Y-%m-%d').strftime(format_date)


def get_percentaje(amount_sale, amount_total):
    """."""
    return '%.2f' % (decimal.Decimal(amount_sale * 100 / amount_total))


def get_commission(percentaje, amount):
    """."""
    return amount * percentaje / 100


def get_date_start():
    """."""
    return '{}-01-01'.format(datetime.now(tz).year)


def valid_date(date_from, date_to):
    """."""
    if date_from > date_to:
        raise UserError(_('Error in the selection of dates.'))


def order_commission(dicc):
    """."""
    return sorted(dicc.items(), key=lambda kv: kv[1], reverse=True)
