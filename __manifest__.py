# Copyright (c) 2023-Present Autodidacta TI. (<https://autodidactati.com>)

{
    'name': 'Reporte Precios de Venta sin actualizar',
    "version": "15.0",
    'author': 'Fernando Morelli - Autodidacta TI',
    'category': 'Extra Tools',
    'license': 'OPL-1',
    'website': 'https://autodidactati.com',
    'summary': 'Reporte Precios de Venta sin actualizar',
    'description': '''Reporte Precios de Venta sin actualizar''',
    'depends': ['purchase'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/report_wizard_view.xml',
    ],
    'installable': True,
    'auto_install': False
 }