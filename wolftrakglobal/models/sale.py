import logging
from datetime import datetime, timedelta
from odoo import api, fields, models, _
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from bs4 import BeautifulSoup
import requests
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = "sale.order"

    def default_ex_rate(self):
        if not self.partner_id and not self.ex_rate:
            return self.env['wolftrak.tools'].default_ex_rate_2()


    ex_rate = fields.Float(string='Tasa de Cambio del dia', digits=(1, 4),
                           default=lambda self: self.default_ex_rate())


    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['ex_rate'] = self.ex_rate
        return invoice_vals

    def currency_exchange(self):
        self.env['wolftrak.tools'].currency_exchange(self)


    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist', required=True, readonly=True,
                                   states={'draft': [('readonly', False)], 'sent': [
                                       ('readonly', False)]},
                                   help="Pricelist for current sales order.", default=2)