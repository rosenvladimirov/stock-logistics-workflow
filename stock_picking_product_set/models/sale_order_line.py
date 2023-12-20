#  Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _prepare_procurement_values(self, group_id=False):
        values = super(SaleOrderLine, self)._prepare_procurement_values(group_id)
        self.ensure_one()
        values.update({
            'product_set_id': self.product_set_id.id,
            'product_set_line_id': self.product_set_line_id.id
        })
        return values
