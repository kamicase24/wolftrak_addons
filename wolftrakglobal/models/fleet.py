# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.modules import get_module_resource
from odoo.exceptions import ValidationError, UserError
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)



class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'


    chassis = fields.Char(string='Chasis')


