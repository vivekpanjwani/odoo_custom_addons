{
    'name':'Employee',
    'version':'1.0.0',
    'depend':['base', 'mail'],
    'license':'LGPL-3',
    'summary':'Employee Module',
    'data':[
        'security/employee_security.xml',
        'security/ir.model.access.csv',
        'views/employee_views.xml',
        'views/emp_designation.xml',
        'views/emp_tag_views.xml',
        'views/employee_contract_view.xml',
        # 'views/employee_menus.xml',
            ],
    'application': True,
    'installable': True,
    'auto_install': False,
    'description': 'Module having employee fields',
    'author': 'Vivek Panjwani',
}

