# Copyright 2023-2025 Rosen Vladimirov, BioPrint Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Stock Picking Product Set',
    'summary': 'Add support for product sets in stock pickings',
    'version': '18.0.1.0.0',
    'category': 'Inventory/Inventory',
    'license': 'AGPL-3',
    'author': 'Rosen Vladimirov, BioPrint Ltd., Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/stock-logistics-workflow',
    'maintainers': ['rosenvladimirov'],
    'development_status': 'Beta',
    'depends': [
        'product_set',
        'sale_product_set',
        'sale_stock',
        'stock',
        'l10n_bg_report_stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/product_set_add.xml',
        'views/stock_picking_views.xml',
        'report/report_accepted_deliveryslip.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
    'post_init_hook': 'post_init_hook',
}
