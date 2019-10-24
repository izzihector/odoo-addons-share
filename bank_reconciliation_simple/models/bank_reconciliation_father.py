# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class BankReconciliationFather(models.Model):
    """Bank Reconciliation Father."""

    _name = 'bank.reconciliation.father'
    _description = "Bank Reconciliation Father"
    _order = 'id desc'

    name = fields.Char('Código', default="New", copy=False)
    bank_id = fields.Many2one('res.bank', 'Banco', copy=False)
    description = fields.Char('Descripción', copy=False)
    date = fields.Date('Fecha')
    obs = fields.Text('Observación')
    saldo_inicial = fields.Float('Saldo Inicial', copy=False)
    saldo_final = fields.Float('Saldo Final', copy=False)
    entry_date = fields.Datetime(
        'Fecha de Entrada', readonly=True, default=fields.Datetime.now)
    user_id = fields.Many2one(
        'res.users', string='Creado', readonly=True,
        default=lambda self: self.env.user)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('conciliado', 'Conciliado')],
        string='Estatus', readonly=True, default='draft', copy=False)
    lines_ids = fields.One2many(
        'bank.reconciliation.simple', 'reconciliation_id', string='Líneas')

    @api.multi
    def exe_conciliar(self):
        """."""
        for record in self:
            for line in self.lines_ids:
                if line.state != 'conciliado':
                    raise ValidationError(
                        'No puede cerrar una cartola con Movimientos'
                        ' no Conciliados !')
        record.state = 'conciliado'

    @api.multi
    def exe_romper_conciliacion(self):
        """."""
        for record in self:
            record.state = 'draft'

    @api.multi
    def exe_draft(self):
        """."""
        for record in self:
            record.state = 'draft'

    @api.model
    def create(self, vals):
        """."""
        if vals.get('name', "New") == "New":
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'bank.reconciliation.father') or "New"
        return super(BankReconciliationFather, self).create(vals)

    @api.multi
    def unlink(self):
        """."""
        for record in self:
            if record.state == 'conciliado':
                raise ValidationError(
                    'No se pueden eliminar Cartolas en estado conciliado.')
            if record.lines_ids.filtered(lambda a: a.state == 'conciliado'):
                raise ValidationError(
                    'No se pueden eliminar Cartolas con '
                    'lineas en estado conciliado.')
        return super(BankReconciliationFather, self).unlink()
