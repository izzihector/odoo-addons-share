# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class BankReconciliationSimple(models.Model):
    """Bank Reconciliation Simple."""

    _name = 'bank.reconciliation.simple'
    _description = "Bank Reconciliation Simple"
    _order = 'id desc'

    name = fields.Char('Código', default="New", copy=False)
    description = fields.Char('Descripción', copy=False)
    date = fields.Date('Fecha')
    voucher = fields.Float('Número Voucher', copy=False)
    no_doc = fields.Char('No Documento', copy=False)
    abono = fields.Float('Abono')
    cargo = fields.Float('Cargo')
    account_move_line_id = fields.Many2one('account.move.line', copy=False)
    obs = fields.Text('Observación')
    invoice_id = fields.Many2one('account.invoice', copy=False)
    partner_id = fields.Many2one('res.partner', copy=False)
    bank_id = fields.Many2one('res.bank', 'Banco', copy=False)
    entry_date = fields.Datetime(
        'Fecha de Entrada', readonly=True, default=fields.Datetime.now)
    user_id = fields.Many2one(
        'res.users', string='Creado', readonly=True,
        default=lambda self: self.env.user)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('conciliado', 'Conciliado'),
        ('cancel', 'Cancelado')],
        string='Estatus', readonly=True, default='draft', copy=False)
    type = fields.Selection([
        ('abono', 'Abono'),
        ('cargo', 'Cargo'),
        ('cheque', 'Cheque')],
        string='Tipo', index=True, default='abono', copy=False)

    reconciliation_id = fields.Many2one(
        'bank.reconciliation.father', copy=False)

    lines_ids = fields.One2many(
        'bank.reconciliation.simple.lines',
        'reconciliation_line_id', ondelete="restrict", string='Líneas')

    @api.onchange('abono', 'cargo')
    def onchange_partner_id(self):
        """."""
        if self.abono != 0:
            self.type = 'abono'

        if self.cargo != 0:
            self.type = 'cargo'

    @api.model
    def create(self, vals):
        """."""
        if vals.get('name', "New") == "New":
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'bank.reconciliation.simple') or "New"
        return super(BankReconciliationSimple, self).create(vals)

    def exe_conciliar(self):
        """."""
        if self.abono == 0 and self.cargo == 0:
            raise ValidationError(
                'No puede conciliar un mov sin saldos, '
                'favor defina un Deposito un un Cargo')

        record = self.lines_ids.filtered(
            lambda i: i.check is True)

        if len(record) != 1:
            raise ValidationError(
                'Se debe seleccionar un apunte contable!')

        self.account_move_line_id = record.account_move_line_id.id or False

        if not self.account_move_line_id:
            raise ValidationError('No esta cargada la entrada contable')

        self.state = 'conciliado'
        self.account_move_line_id.reconciled = True

        self.lines_ids.unlink()

    @api.multi
    def exe_romper_conciliacion(self):
        """."""
        for record in self:
            record.account_move_line_id.reconciled = False
            record.account_move_line_id = False
            record.state = 'draft'

    @api.multi
    def exe_cancel(self):
        """."""
        for record in self:
            record.state = 'cancel'

    @api.multi
    def exe_draft(self):
        """."""
        for record in self:
            record.state = 'draft'

    def exe_delete_line(self):
        """."""
        self.lines_ids.unlink()

    def exe_account_move_lines(self):
        """."""
        q = 'credit' if self.cargo > self.abono else 'debit'
        amount = self.cargo if self.cargo > self.abono else self.abono
        move_line_obj = self.env['account.move.line']
        simple_lines_obj = self.env['bank.reconciliation.simple.lines']

        move_lines = move_line_obj.search(
            [(q, '=', amount),
             ('can_be_reconciled', '=', True),
             ('reconciled', '=', False)])

        if not move_lines:
            raise ValidationError(
                'No se encontraron posibles apuntes.')

        move_lines_list = []

        self.lines_ids.unlink()

        for i in move_lines:
            simple_lines_id = simple_lines_obj.search(
                [('account_move_line_id', '=', i.id),
                 ('reconciliation_line_id', '=', self.id)])
            if not simple_lines_id:
                move_lines_list.append((0, 0, {'account_move_line_id': i.id}))
        self.lines_ids = move_lines_list

    @api.multi
    def unlink(self):
        """."""
        for record in self:
            if record.state == 'conciliado':
                raise ValidationError(
                    'No se pueden eliminar lineas en estado conciliado.')
        return super(BankReconciliationSimple, self).unlink()


class BankReconciliationSimpleLines(models.Model):
    """Bank Reconciliation Simple Lines."""

    _name = 'bank.reconciliation.simple.lines'
    _description = "Bank Reconciliation Simple Lines"

    reconciliation_line_id = fields.Many2one(
        'bank.reconciliation.simple', 'Linea')

    account_move_line_id = fields.Many2one(
        'account.move.line', 'Apunte')

    currency_id = fields.Many2one(
        'res.currency', related='account_move_line_id.company_id.currency_id',
        string="Company Currency")

    date = fields.Date(
        'Fecha', related='account_move_line_id.date')

    move_id = fields.Many2one(
        'account.move', related='account_move_line_id.move_id',
        string='Asiento Contable')

    journal_id = fields.Many2one(
        'account.journal', related='account_move_line_id.journal_id',
        string='Diario')

    label = fields.Char(
        related='account_move_line_id.name', string='Etiqueta')

    debit = fields.Monetary(
        related='account_move_line_id.debit', string='Debe')

    credit = fields.Monetary(
        related='account_move_line_id.credit', string='Haber')

    reconciled = fields.Boolean(
        related='account_move_line_id.reconciled', string='Conciliado')

    check = fields.Boolean('Check')
