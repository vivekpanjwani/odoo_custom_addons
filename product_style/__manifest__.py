{
    "name": "Product Style",
    "version": "1.0.1",
    "license":"LGPL-3",
    "description": "Product Style ",
    "author":"Vivek Panjwani",
    "depends":['base', 'sale','product'],
    "data":[
        "security/ir.model.access.csv",
        "views/product_style_view.xml",
        "views/business_menu.xml",
        "views/branch_product_data_views.xml",
        "views/product_master_views.xml",
        "views/customer_views.xml",
        "views/customer_sale_order_view.xml",
        "views/sale_order_line_view.xml",


    ],
    "installable": True,
    "application": True,

}