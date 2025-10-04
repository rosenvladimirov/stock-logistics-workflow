#  Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from odoo import models, _

_logger = logging.getLogger(__name__)


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _get_product_set(self):
        product_set_id = self.picking_id.product_set_ids.filtered(lambda r: r.product_set_id == self.move_id.product_set_id)
        quantity = sum([x.product_qty for x in self.picking_id.move_ids.filtered(lambda r: r.product_set_id)])
        return product_set_id and product_set_id or self.env['picking.product.set'], quantity

    @staticmethod
    def _get_aggregated_set_properties(move_line=False, move=False):
        move = move or move_line.move_id
        uom = move.product_uom or move_line.product_uom_id
        name = move.product_set_id.display_name
        description = move.description_picking
        if description == name or description == move.product_id.name:
            description = False
        product_set_id = move.product_set_id
        line_key = f'{product_set_id.id}_{product_set_id.ref and product_set_id.ref or ""}_{""}_{uom.id}'
        return line_key, name, description, uom

    def _get_aggregated_product_quantities(self, **kwargs):
        aggregated_move_lines = super()._get_aggregated_product_quantities(**kwargs)
        for move_line in self.filtered(lambda r: r.move_id.product_set_id):
            aggregated_set_properties = self._get_aggregated_set_properties(move=move_line.move_id)
            line_key = aggregated_set_properties[0]
            if line_key not in aggregated_move_lines:
                if not aggregated_move_lines.get(line_key):
                    product_set_ids = move_line.picking_id.product_set_ids.filtered(
                        lambda r: r.product_set_id == move_line.move_id.product_set_id)
                    quantity_set = sum([x.quantity for x in product_set_ids])
                    uom = move_line.product_uom_id
                    quantity_total = sum(x.product_uom._compute_quantity(x.product_qty, uom) for x in move_line.picking_id.move_ids.filtered(lambda r: r.product_set_id))
                    aggregated_move_lines[line_key] = {
                        "name": aggregated_set_properties[1],
                        "description": aggregated_set_properties[2],
                        "product_uom": aggregated_set_properties[3],
                        "qty_done": quantity_total,
                        "qty_set": quantity_set,
                        'product_set_ids': move_line.move_id.product_set_id,
                    }
        _logger.info(f"aggregated_move_lines {aggregated_move_lines}")
        return aggregated_move_lines
