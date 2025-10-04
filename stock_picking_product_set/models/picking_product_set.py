#  Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, _


class PickingProductSet(models.Model):
    _name = 'picking.product.set'
    _description = 'Stock Picking Sets'

    picking_id = fields.Many2one('stock.picking', 'Picking', required=True)
    product_set_id = fields.Many2one('product.set', 'Product Set')
    quantity = fields.Float('Quantity', digits='Product Unit of Measure')

    @staticmethod
    def _get_picking_product_set_value(picking_id, product_set_id, quantity):
        return {
            'picking_id': picking_id.id,
            'product_set_id': product_set_id.id,
            'quantity': quantity,
        }
