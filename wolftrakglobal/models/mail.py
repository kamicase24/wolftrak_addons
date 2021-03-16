# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _


class MailMessage(models.Model):
    _inherit = "mail.message"

    call_duration = fields.Float(string="Duración de la Llamada", digits=(2, 2))


class MailActivity(models.Model):
    _inherit = "mail.activity"

    call_duration = fields.Float(string='Duración de la Llamada', digits=(2, 2))

    # To-Do migrate this methos once instaled
    # @api.model
    # def action_log(self):
    #     for log in self:
    #         body_html = f"<div><b>%(title)s</b>: %(next_activity)s</div><div><b>Duración de la llamada: </b>%(call_duration)s</div>%(description)s%(note)s" % {
    #             'title': _('Activity Done'),
    #             'next_activity': log.next_activity_id.name,
    #             'description': log.title_action and '<p><em>%s</em></p>' % log.title_action or '',
    #             'note': log.note or '',
    #             'call_duration': str(log.call_duration)
    #         }
    #         log.lead_id.message_post(
    #             body_html,
    #             subject=log.title_action,
    #             subtype_id=log.next_activity_id.subtype_id.id,
    #             call_duration=log.call_duration)

    #         log.lead_id.write({
    #             'date_deadline': log.date_deadline,
    #             'planned_revenue': log.planned_revenue,
    #             'title_action': False,
    #             'date_action': False,
    #             'next_activity_id': False,
    #             'call_duration': log.call_duration
    #         })
    #     return True
