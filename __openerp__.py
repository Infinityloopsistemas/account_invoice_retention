# -*- coding: utf-8 -*-
{
    'name': "Invoice Retention Guarentee",

    'summary': """
        Genera las retenciones por garantias, epsecificas sector construccion""",

    'description': """Estas retenciones se practican sobre facturaciones en el ramo de la construcción ,son para garantizar la calidad de la obra, por lo general el periodo es de un año.
        Existen 2 escenarios el DE OBRA FINALIZADA  y en CURSO por lo que en el primero la retencion se resta del total de la factura con impuesto, y en la segunda se resta solo de
        la base imponible y a posterior se calcula el impuesto.
    """,

    'author': "Infinityloop Sistemas",
    'website': "http://www.infinityloop.es",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Finananzas',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [ 'views/account_invoice.xml',
              'reports/account_report.xml',
              'reports/report_invoice_retention.xml'
        # 'security/ir.model.access.csv',



    ],
    # only loaded in demonstration mode

    'installable': True,
    'auto_install': False,
}