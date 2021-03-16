# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.modules import get_module_resource
from odoo.exceptions import ValidationError, UserError
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)



class MobileDevice(models.Model):
    _name = 'mobile.device'
    _description = 'Dispositivos Móviles'

    @api.onchange('mobile_brand_id')
    def get_domain_mobile_model_id(self):
        return {
            'domain': {
                'mobile_model_id': [('mobile_brand_id', '=', self.mobile_brand_id.id)]
            }
        }

    name = fields.Char(string='Disp. Móvil', required=True)
    mobile_brand_id = fields.Many2one('mobile.brand', string='Marca de Disp. Móvil')
    mobile_model_id = fields.Many2one('mobile.model', string='Modelo de Disp. Móvil')
    imei = fields.Char(string='IMEI', help='International Mobile Station Equipment Identity')
    batery = fields.Char(string='Batería')
    batery_serial = fields.Char(string='Serial de la Batería')
    batery_model = fields.Char(string='Modelo de la Batería')
    employee_id = fields.Many2one('hr.employee', string='Empleado',
                                  help='Empleado Asignado a este número de telefono')
    number = fields.Char(string='Número asociado')
    simcard_imei = fields.Char(string='IMEI de la Simcard')



class MobileBrand(models.Model):
    _name = 'mobile.brand'
    _description = 'Marca de Disp. Móvil'

    name = fields.Char(string='Marca', required=True)
    note = fields.Text(string='Nota')
    mobile_model_id = fields.Many2one('mobile.model', string='Modelo de Disp. Móvil')


class MobileModel(models.Model):
    _name = 'mobile.model'
    _description = 'Modelo de Disp. Móvil'

    name = fields.Char(string='Modelo', required=True)


