#  Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _


class StockMove(models.Model):
    _inherit = "stock.move"

    product_set_id = fields.Many2one('product.set', string='Product set')
    product_set_line_id = fields.Many2one('product.set.line', string='Product set line')

    @api.model
    def _prepare_merge_moves_distinct_fields(self):
        return super(StockMove, self)._prepare_merge_moves_distinct_fields() + ['product_set_id', 'product_set_line_id']
