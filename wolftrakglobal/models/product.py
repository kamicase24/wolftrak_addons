# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError, AccessError
_logger = logging.getLogger(__name__)


# SE USARA PROCESO DE PAQUETE DE ODOO
# class ProductWolftrak(models.Model):
#     _inherit = "product.template"

    # type = fields.Selection(selection_add=[('pack', 'Paquete')])

    # pack_line_ids = fields.One2many('pack.line.wolftrak', 'product_id', string='Productos')
    # pack_code = fields.Char(string='Pack #')


    # SE USARA PROCESO DE PAQUETE DE ODOO
    # def _compute_currency_id(self):
    #     for template in self:
    #         template.currency_id = self.env['res.currency'].search([('name', '=', 'USD')], limit=1)


# SE USARA PROCESO DE PAQUETE DE ODOO
# class PackLineWolftrak(models.Model):
#     _name = 'pack.line.wolftrak'
#     _description = 'Paquete Wolftrak'

#     @api.onchange('pack_item_id')
#     def _set_values(self):
#         if self.pack_item_id:
#             self.description = self.pack_item_id.name

#     product_id = fields.Many2one('product.template', string='Producto Padre')
#     pack_item_id = fields.Many2one('product.template', string='Item')
#     name = fields.Char(string='Descripción')
#     quantity = fields.Float(string='Cantidad', default=1.0)
#     list_price = fields.Float(string='Precio de Venta', related="pack_item_id.list_price")
#     uom_id = fields.Many2one('product.uom', string='Unidad de Medida', related="pack_item_id.uom_id")
#     currency_id = fields.Many2one('res.currency', string='Moneda', realted='pack_item_id.currency_id')


# DEPRECATED METHOD...
# class ProductProductWolftrak(models.Model):
#     _inherit = 'product.product'

    # @api.multi
    # def _need_procurement(self):
    #     for product in self:
    #         if product.type not in ['service', 'digital', 'pack']:
    #             return True
    #     return super(ProductProductWolftrak, self)._need_procurement()
