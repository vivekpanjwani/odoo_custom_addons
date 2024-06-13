{
    "name": "Zone Management",
    "version": "1.0.1",
    "license":"LGPL-3",
    "description": "Zone Manegement",
    "summary":"Zone",
    "author":"Vivek Panjwani",
    "depends":['base', 'sale', 'contacts'],
    "data":[
        "views/res_partner_zone.xml",
        "views/zone_views.xml",
        "views/zone_zips.xml",
        "views/stock_picking_inherit.xml",

        "security/ir.model.access.csv"

    ],
    "installable": True,
    "application": True,

}