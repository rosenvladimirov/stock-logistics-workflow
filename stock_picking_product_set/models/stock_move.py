#  Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _name = 'stock.move'
    _inherit = ["stock.move", "product.set.mixin"]

    @api.model
    def _prepare_merge_moves_distinct_fields(self):
        return super(StockMove, self)._prepare_merge_moves_distinct_fields() + ['product_set_id', 'product_set_line_id']
