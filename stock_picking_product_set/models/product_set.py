#  Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models


class ProductSet(models.Model):
    _inherit = "product.set"

    def prepare_stock_picking_values(self, sequence):
        self.ensure_one()
        return {
            "sequence": sequence,
            "name": self.display_name,
            "product_set_id": self.id,
        }
