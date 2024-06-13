# -*- coding: utf-8 -*-
{
    'name': "tour",

    'summary': """
        Tour Packages""",

    'description': """
        Tour
    """,

    'author': "Vivek Panjwani",
    'version': "1.0.1",
    'license': "LGPL-3",

    'depends': ['base', 'product', 'sale'],

    'data': [
        'security/ir.model.access.csv',

        'data/ir_sequence_tour.xml',

        'views/tour_package_views.xml',
        'views/tour_views.xml',
        
    ],

    "installable": True,
    "application": True,

}
