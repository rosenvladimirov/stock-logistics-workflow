# Copyright 2015 Anybox S.A.S
# Copyright 2016-2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductSetLine(models.Model):
    _inherit = "product.set.line"

    def prepare_stock_move_values(self, picking, quantity, max_sequence=0):
        self.ensure_one()
        return {
            "order_id": picking.id,
            "product_set_id": self.product_set_id.id,
            "product_id": self.product_id.id,
            "product_uom_qty": self.quantity * quantity,
            "product_uom": self.product_id.uom_id.id,
            "sequence": max_sequence + self.sequence,
            "company_id": self.company_id.id,
            "product_set_line_id": self.id
        }
