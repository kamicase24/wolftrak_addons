# -*- coding: utf-8 -*-

from odoo import fields, api, models


class WolftrakDailyJournal(models.TransientModel):
    _name = 'wolftrak.daily.journal'
    _description = 'Libro Diario de Wolftrak'

    def default_move(self):
        return self.env['account.move'].search([])

    def default_move_line(self):
        return self.env['account.move.line'].search([])

    date_from = fields.Date(string="Fecha de Inicio")
    date_to = fields.Date(string="Fecha de Fin")
    move_ids = fields.Many2many("account.move", default=default_move)
    move_line_ids = fields.Many2many("account.move.line")

    @api.onchange('date_from', 'date_to')
    def _onchange_date(self):
        self.move_ids = self.env['account.move'].search([('date', '>=', self.date_from), ('date', '<=', self.date_to)])
        self.move_line_ids = self.move_ids.mapped('line_ids')

        # for move in self.move_id:
        #     self.move_line_id += self.env['account.move.line'].search(
        #         [('move_id', '=', move.id)])


    @api.model
    def render_html(self, docids, data=None):
        # model = self.env.context.get('active_model')
        # docs = self.env[model].browse(self.env.context.get('active_id'))

        report_obj = self.env['report']
        report = report_obj._get_report_from_name(
            'wolftrakglobal.daily_journal')

        docargs = {
            'doc_ids': self.ids,
            'doc_model': report.model,
            'docs': self.read(),
        }

        return {
            'type': 'ir.actions.report.xml', 
            'report_name': 'wolftrakglobal.daily_journal', 
            'datas': docargs
        }
