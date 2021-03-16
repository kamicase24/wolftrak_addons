# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError
from requests.exceptions import ConnectionError, HTTPError, Timeout

import requests
import json
import sys
import os
from bs4 import BeautifulSoup
_logger = logging.getLogger(__name__)

# main_base = os.path.dirname(os.path.abspath(__file__))
# CONFIG_FILE_NAME = "config.json"
# CONFIG_FILE = os.path.join(main_base, CONFIG_FILE_NAME)
#
#
# def load_config(json_file):
#     with open(json_file, 'r') as file:
#         config_data = json.load(file)
#     return config_data
#
#
# def get_rnc_record(rnc, config_data = None):
#
#     if not config_data:
#         config_data = load_config(CONFIG_FILE)
#     req_headers = config_data['request_headers']
#     # req_cookies = config_data.get('request_cookies')
#     req_params = config_data['request_parameters']
#     uri = ''.join([config_data['url'], config_data['web_resource']])
#
#     req_params['txtRncCed'] = rnc
#     result = requests.get(uri, params = req_params, headers=req_headers)
#     if result.status_code == requests.codes.ok:
#         soup = BeautifulSoup(result.content)
#         data_rows  = soup.find('tr', attrs={'class': 'GridItemStyle'})
#         try:
#             tds = data_rows.findChildren('td')
#             rnc_vals = [str(td.text.strip()) for td in tds]
#             # rnc = Rnc(rnc_vals)
#             return rnc_vals
#         except :
#             pass


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _total_device(self):
        for res in self:
            device_ids_count = self.env['gps.device'].search_count(
                [('partner_id', '=', res.id)])
            res.total_device = device_ids_count


    def _default_user_id(self):
        return self.env.uid

    def _compute_tags(self):
        for res in self:
            leads = self.env['crm.lead'].search([('partner_id', '=', res.id)])
            tags = leads.mapped('tag_ids')
            res.tag_ids = [(4, 0, tag_id) for tag_id in tags]


    def update_fields(self):
        leads = self.env['crm.lead'].search([('partner_id', 'in', self.ids)])
        for lead in leads:
            _logger.info(lead)
            if lead.street and not self.street:
                self.street = lead.street
            if lead.street2 and not self.street2:
                self.street2 = lead.street2
            if lead.city and not self.city:
                self.city = lead.city
            if lead.country_id and not self.country_id:
                self.contry_id = lead.country_id
            if lead.state_id and not self.state_id:
                self.state_id = lead.state_id
            if lead.zip and not self.zip:
                self.zip = lead.zip
            if lead.email_from and not self.email:
                self.email = lead.email_from
            if lead.phone and not self.phone:
                self.phone = lead.phone
            if lead.alias and not self.alias:
                self.alias = lead.alias

    def _get_invoices(self):
        for res in self:
            invoice_ids = self.env['account.invoice'].search(
                [('partner_id', '=', res.id)])
            res.partner_invoice_ids = [(4, 0, inv_id)
                                       for inv_id in invoice_ids.mapped('id')]

    doc_ident = fields.Char(string='Documento de Identificación')
    dgii_state = fields.Char(string='Estado')
    pay_reg = fields.Char(string='Regimen de Pago')
    doc_ident_type = fields.Integer(string='Tipo de Documento')
    user_id = fields.Many2one(
        'res.users', string='Comercial', default=_default_user_id)
    total_device = fields.Integer(
        string='Dispositivos', help='Total de dispositivos vendidos a este cliente', compute=_total_device)
    start_date = fields.Date(string='Fecha de Inicio',
                             help='Fecha en que inicio el contrato el cliente.')
    alias = fields.Char(string='Razón Comercial')
    tag_ids = fields.Many2many(
        'crm.lead.tag', string='Categoría', compute=_compute_tags)
    partner_inv = fields.Many2many('account.invoice', compute=_get_invoices)

    @api.onchange('doc_ident')
    def onchange_ident_doc(self):
        if self.doc_ident:
            if len(self.doc_ident) == 11:
                self.doc_ident_type = 2
            elif len(self.doc_ident) == 9:
                self.doc_ident_type = 1

        try:
            print(self.doc_ident)
            rnc_record = self.env['wolftrak.tools'].get_rnc_record(self.doc_ident)
            self.name = rnc_record[1]
            self.dgii_state = rnc_record[5]
            self.pay_reg = rnc_record[4]
        except (ConnectionError, HTTPError) as e:
            _logger.warning(f'Error Http {e}')
            raise Warning(f'Error Http {e}')
        except (ConnectionError, Timeout) as e:
            _logger.warning(e)
            _logger.warning('El tiempo de envío se ha agotado.')
            raise Warning('El tiempo de envío se ha agotado.')
        except Exception as e:
            _logger.warning(e)
            

    @api.constrains('doc_ident', 'phone')
    def parter_validation(self):
        if self.search([('doc_ident', '=', self.doc_ident), ('id', '!=', self.id)]):
            raise ValidationError('Ya existe un Cliente registrado bajo este número de documento.')
        if self.search([('doc_ident', '=', self.doc_ident), ('id', '!=', self.id)]):
            raise ValidationError('Ya existe un Cliete registrado bajo este número de teléfono.')


    def device_history(self):
        action = self.env.ref('wolftrakglobal.action_partner_device_lines')
        result = action.read()[0]
        result['domain'] = [('partner_id', 'in', self.ids)]
        return result

    @api.depends('country_id')
    def _compute_product_pricelist(self):
        for p in self:
            if not isinstance(p.id, models.NewId):  # if not onchange
                p.property_product_pricelist = self.env['product.pricelist'].search([
                                                                                    ('id', '=', 2)])



class ResCompany(models.Model):
    _inherit = 'res.company'


    report_path = fields.Char(string='Ruta para la creación de archivo TXT de reportes (606 / 607)')