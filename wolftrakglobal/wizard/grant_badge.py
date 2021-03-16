# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, exceptions

class GamificationBadgeUserWizard(models.TransientModel):
    _inherit = 'gamification.badge.user.wizard'

    success_rate = fields.Integer(string="Porcentaje de exito")

    @api.model
    def action_grant_badge(self):
        """Wizard action for sending a badge to a chosen employee"""

        if not self.user_id:
            raise exceptions.UserError(_('You can send badges only to employees linked to a user.'))

        if self.env.uid == self.user_id.id:
            raise exceptions.UserError(_('You can not send a badge to yourself'))

        values = {
            'user_id': self.user_id.id,
            'sender_id': self.env.uid,
            'badge_id': self.badge_id.id,
            'employee_id': self.employee_id.id,
            'comment': self.comment,
            'success_rate': self.success_rate
        }

        return self.env['gamification.badge.user'].create(values)._send_badge()
