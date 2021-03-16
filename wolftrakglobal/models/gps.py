# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.modules import get_module_resource
from odoo.exceptions import ValidationError, UserError
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)



class GpsDevice(models.Model):
    _name = 'gps.device'
    _description = 'Dispositivo GPS'

    @api.model
    def _get_default_image(self):
        colorize, img_path, image = False, False, False
        if not image:
            img_path = get_module_resource('wolftrakglobal', 'static/src/img', 'gps.png')
            colorize = True
        if img_path:
            with open(img_path, 'rb') as f:
                image = f.read()
        if image and colorize:
            image = tools.image_colorize(image)

        return tools.image_resize_image_medium(image.encode('base64'))


    @api.onchange('partner_id')
    def _get_default_invoices(self):
        for res in self:
            res.invoice_ids = res.env['account.invoice'].search([('partner_id', '=', res.partner_id.id)])


    def _default_start_date(self):
        if self.partner_id and self.partner_id.start_date:
            return self.partner_id.start_date

    def _default_currency(self):
        currency_id = self.env.user.company_id.currency_id.id
        return currency_id

    def set_partner_dateprice(self):
        if self.partner_id:
            if self.partner_id.start_date:
                self.start_date = self.partner_id.start_date
            else:
                raise UserError(_("El cliente no posee Fecha de inicio de servicio."))
            
            first_invoice = self.invoice_ids.filtered(lambda i: 
                    (i.date_invoice.month == self.start_date.month) and 
                    (i.date_invoice.year == self.start_date.year)) 
            if first_invoice:

                unit_price = 0.0
                # Establece el precio unitario desde la linea con el prodcuto GPS
                # de la primera factura generada. Es necesario establecer 
                # el producto GPS posea el campo default_code = 'GPS', 
                # de lo contrario, no encontrará producto alguno
                gps_product_id = first_invoice.invoice_line_ids.filtered(lambda l: 
                    l.product_id.default_code == 'GPS')
                if gps_product_id:
                    if len(gps_product_id) > 1:
                        gps_product_id = gps_product_id[1]
                    unit_price = gps_product_id.price_unit
                    month_payment = unit_price
                    
                monthly_payment = 0.0
                # Establece el pago mensual desde el producto que representa
                # la mensualidad en la linea de la primera factura generada. 
                # Es necesario que el producto sea de tipo servicio y posea
                # el campo default_code = 'MP' (de Monthly Payment).
                monthly_payment_prod_id = first_invoice.invoice_line_ids.filtered(lambda l: 
                    (l.product_id.defualt_code == 'MP') and 
                    (l.product_id.type == 'service'))
                self.gps_month_payment = month_payment
                self.gps_price = unit_price
            else:
                raise UserError(("El cliente no posee facturas"))
        else:
            raise UserError(("Seleccione un Cliente por favor"))


    name = fields.Char(string='Ficha GPS', required=True)
    image = fields.Binary(string="Imagen", default=_get_default_image)
    gps_brand_id = fields.Many2one('gps.brand', string='Marca de GPS')
    gps_model_id = fields.Many2one('gps.model', string='Modelo de GPS')
    imei = fields.Char(string='IMEI del GPS', help='International Mobile Station Equipment Identity')
    esn = fields.Char(string='ESN')
    sn = fields.Char(string='S/N')

    device_num = fields.Char(string='Número Asignado')
    sim_imei = fields.Char(string='IMEI SIMCARD')

    gps_price = fields.Float(string='Precio del Dispositivo')
    project_id = fields.Char(string='Proyecto')
    note = fields.Text(string='Nota Interna')
    gps_month_payment = fields.Float(string='Mensualidad del Dispositivo')
    currency_id = fields.Many2one('res.currency', string='Moneda', default=_default_currency)
    start_date = fields.Date(string='Fecha de Inicio',
                             help='Fecha en que inicio el contrato el cliente',
                             default=_default_start_date)
    invoice_ids = fields.Many2many('account.invoice', compute=_get_default_invoices)
    status = fields.Selection([('on', 'Activado'),
                               ('off', 'Desactivado'),
                               ('personal', 'Personal'),
                               ('garage', 'Taller'),
                               ('check', 'Verificar')],
                              string='Estado', readonly=True, default='on') 
    partner_id = fields.Many2one('res.partner', string='Cliente')
    alias = fields.Char(string='Razón Comercial', related='partner_id.alias', store=True)

    fleet_vehicle_id = fields.Many2one('fleet.vehicle', string='Vehiculo')

    # All this fields now are related from the fleet_vehicle in order to 
    # use this model to manage all the vehicles within the GPS model
    chassis = fields.Char(string='Chasis', related='fleet_vehicle_id.chassis')
    license_plate = fields.Char(string='Placa', related='fleet_vehicle_id.license_plate') # vehicle model has this field
    vehicle_model_id = fields.Many2one('fleet.vehicle.model', string='Modelo del Vehiculo', related='fleet_vehicle_id.model_id') # vehicle model has this field
    # vehicle_brand_id = fields.Many2one('fleet.vehicle.model.brand', string='Marca del Vehiculo') # vehicle model has this field
    year = fields.Char(string='Año del Vehiculo', related='fleet_vehicle_id.model_year') # vehicle model has this field

    def status_on(self):
        self.status = 'on'

    def status_off(self):
        self.status = 'off'


class GpsBrand(models.Model):
    _name = 'gps.brand'
    _description = 'Marca de GPS'

    name = fields.Char(string='Marca')
    note = fields.Text(string='Nota')
    gps_model_id = fields.Many2one('gps.model', string='Modelo')
    supplier = fields.Many2one('res.partner', string='Proveedor',
                               domain=[('supplier', '=', True), ('customer', '=', False)])


class GpsModel(models.Model):
    _name = 'gps.model'
    _description = 'Modelo de GPS'

    name = fields.Char(string='Modelo')
    note = fields.Text(string='Nota')
