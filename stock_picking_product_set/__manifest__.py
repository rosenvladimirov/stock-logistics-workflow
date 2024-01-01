# Copyright 2023 Rosen Vladimirov, BioPrint Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Stock Picking Product Set',
    'summary': """
        Add support for product set in pickings""",
    'version': '16.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Rosen Vladimirov, BioPrint Ltd.,Odoo Community Association (OCA)',
    'website': 'https://github.com/oca/stock-logistics-workflow',
    'depends': [
        'product_set',
        'sale_product_set',
        'sale_stock',
        'stock',
        'report_accepted_delivery',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/product_set_add.xml',
        'views/stock_picking_views.xml',
        'report/report_accepted_deliveryslip.xml',
    ],
    'demo': [
    ],
    'post_init_hook': 'post_init_hook',
}
