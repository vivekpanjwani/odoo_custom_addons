# -*- coding: utf-8 -*-
{
    "name": "Sale Commission",
    "version": "1.0.1",
    "license":"LGPL-3",
    "description": "Sale Commission to Sale Person",
    "summary":"Sale Commission",
    "author":"Vivek Panjwani",
    'depends': ['base', 'sale', 'account'],
    'application': True,
    'installable': True,
    'data': [
        'security/ir.model.access.csv',

        'views/views_res_users.xml',
        'views/views_sale_order.xml',
        'views/inherit_account_payment_view.xml',

        'report/sale_commission_report.xml',
        'report/ir_action_report_sale_commission.xml',

        'wizard/view_sale_commission_wizard.xml',


    ],

}
