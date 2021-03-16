# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, exceptions

class GamificationBadgeUser(models.Model):
    _inherit = 'gamification.badge.user'

    success_rate = fields.Integer(string="Porcentaje de exito")


class GamificationBadge(models.Model):
    _inherit = 'gamification.badge'

    badge_value = fields.Integer(string="Valor de la Insignea")