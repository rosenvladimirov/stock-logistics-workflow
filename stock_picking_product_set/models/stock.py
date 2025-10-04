#  Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _get_custom_move_fields(self):
        res = super(StockRule, self)._get_custom_move_fields()
        res += ['product_set_id', 'product_set_line_id']
        return res
