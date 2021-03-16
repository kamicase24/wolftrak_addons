# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
_logger = logging.getLogger(__name__)


class WolftrakPurchase(models.Model):
    _inherit = 'purchase.order'

    # BAD PRACTICE... must not use DB ID as VALUES
    # @api.onchange('partner_id')
    # def _set_custom_currency(self):
    #     if self.currency_id.name == 'DOP':
    #         self.currency_id = 3

    def currency_exchange(self):
        self.env['wolftrak.tools'].currency_exchange(self)

    def default_ex_rate(self):
        if not self.partner_id and not self.ex_rate:
            return self.env['wolftrak.tools'].default_ex_rate_2()

    ex_rate = fields.Float(string='Tasa de Cambio', digits=(1, 4), default=lambda self: self.default_ex_rate())


    @api.onchange('partner_id', 'company_id')
    def onchange_partner_id(self):
        if not self.partner_id:
            self.fiscal_position_id = False
            self.payment_artner_id = False
            self.currency_id = False
        else:
            self.fiscal_position_id = self.env['account.fiscal.position'].with_context(company_id=self.company_id.id).get_fiscal_position(self.partner_id.id)
            self.payment_term_id = self.partner_id.property_supplier_payment_term_id.id

            # BAD PRACTICE... must not use DB ID as VALUES
            # if self.currency_id.name == 'DOP' or not self.currency_id:
            #     self.currency_id = 3
        return {}
