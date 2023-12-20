#  Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from odoo import api, fields, models, _
from odoo.tools import groupby

_logger = logging.getLogger(__name__)


class Picking(models.Model):
    _inherit = "stock.picking"

    product_set_ids = fields.Many2many('picking.product.set',
                                       compute="_compute_product_set_ids",
                                       string="Product sets")

    @api.depends('move_ids')
    def _compute_product_set_ids(self):
        compensation_product_id = self.with_company(self.env.company). \
            env.ref('product_set.compensation_product', raise_if_not_found=False).id
        for record in self:
            _logger.info(f"ORDER LINE {record}:{record.move_ids}")
            record.product_set_ids = False
            if not record.id:
                continue

            for product_set_id, lines in groupby(record.move_ids.sorted(lambda r: r.product_set_id.id),
                                                 key=lambda r: r.product_set_id):
                if not product_set_id:
                    continue
                # line_product_set_id = product_set_id
                quantity = sum([l.quantity for l in product_set_id.set_line_ids.filtered(
                    lambda r: r.product_id.id == compensation_product_id)]) or 1.0
                total_quantity = 0.0
                for stock_move_id in lines:
                    if stock_move_id.product_id.id == compensation_product_id:
                        if stock_move_id.state == 'done':
                            total_quantity += stock_move_id.quantity_done
                        else:
                            total_quantity += stock_move_id.product_uom_qty

                _logger.info(f"VALUES {record}:{lines}:{product_set_id}:{total_quantity}:{quantity}")
                record.product_set_ids |= self.env['picking.product.set'].create(
                    self.env['picking.product.set']._get_picking_product_set_value(
                        record,
                        product_set_id,
                        total_quantity / quantity,
                    ))
