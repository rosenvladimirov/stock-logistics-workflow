#  Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _


class StockMove(models.Model):
    _name = 'stock.move'
    _inherit = ["stock.move", "product.set.mixin"]

    @api.model
    def _prepare_merge_moves_distinct_fields(self):
        return super(StockMove, self)._prepare_merge_moves_distinct_fields() + ['product_set_id', 'product_set_line_id']

    def _get_aggregated_values(self, name, description, qty_done, qty_ordered, uom):
        values = super()._get_aggregated_values(name, description, qty_done, qty_ordered, uom)
        product_set_id = self.product_set_id
        product_set_ids = self.picking_id.product_set_ids.filtered(lambda r: r.product_set_id.id == product_set_id.id)
        if product_set_ids:
            values.update({
                'product_set_id': self.product_set_id,
                'product_set_qty': sum([x.quantity for x in product_set_ids])
            })
        return values


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _get_aggregated_keys(self, move):
        line_key = super()._get_aggregated_keys(move)
        if move.product_set_id:
            line_key = f"{move.product_set_id}_{line_key}"
        return line_key

    def _get_aggregated_values(self, name, description, qty_done, qty_ordered, uom):
        values = super()._get_aggregated_values(name, description, qty_done, qty_ordered, uom)
        product_set_id = self.move_id.product_set_id
        product_set_ids = self.picking_id.product_set_ids.filtered(lambda r: r.product_set_id.id == product_set_id.id)
        if product_set_ids:
            values.update({
                'product_set_id': product_set_id,
                'product_set_qty': sum(x.quantity for x in product_set_ids),
            })
        return values

    def _get_aggregated_product_quantities(self, **kwargs):
        def get_aggregated_properties(move_line=False, move=False):
            move = move or move_line.move_id
            uom = move.product_uom or move_line.product_uom_id
            name = move.product_id.display_name
            description = move.description_picking
            if description == name or description == move.product_id.name:
                description = False
            product = move.product_id
            line_key = f'{product.id}_{product.display_name}_{description or ""}_{uom.id}'
            return (line_key, name, description, uom)

        aggregated_move_lines = super()._get_aggregated_product_quantities(**kwargs)
        for move_line in self:
            line_key = get_aggregated_properties(move_line=move_line)
            product_set_ids = move_line.picking_id.move_ids. \
                filtered(lambda r: r.product_id.id == move_line.product_id.id).mapped('product_set_id')
            if line_key in aggregated_move_lines:
                aggregated_move_lines[line_key]["product_set_ids"] = product_set_ids
        return aggregated_move_lines
