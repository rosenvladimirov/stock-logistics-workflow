#  Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    for line in env['stock.move'].search([]):
        line.write({
            'product_set_id': line.sale_line_id.product_set_id.id,
            'product_set_line_id': line.sale_line_id.product_set_line_id.id
        })
