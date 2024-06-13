{
    "name": "Employee Management",
    "version": "1.0.1",
    "license":"LGPL-3",
    "description": "Employee Manegement",
    "summary":"Employee New",
    "author":"Vivek Panjwani",
    "depends":['base','mail','sale','web_map','contacts','purchase', 'website'],
    "data":[
        "security/emp_security.xml",
        "security/ir.model.access.csv",

        "data/ir_sequence_data_emp.xml",
        "data/emp_ir_cron.xml",
        "data/demo_product.xml",
        "data/employee_mail_template_new.xml",

        "wizard/emp_pay_wizard_view.xml",
        "wizard/emp_data_export.xml",

        "report/purchase_order_report_view.xml",
        "report/payslip_report_views.xml",
        "report/report_employee_action.xml",


        "views/view_website_menu.xml",
        "views/sale_model_field_view.xml",
        "views/product_purchase_po.xml",
        "views/city.xml",
        "views/personal_info.xml",
        "views/tags_views.xml",
        "views/designation.xml",
        "views/emp_contract.xml",
        "views/res_config_setting_view.xml",
        "views/emp_views.xml",
        "views/payslip_bill_report_document.xml",
        "views/employee_portal_template.xml",
        "views/employee_report_template.xml",
        "views/website_product_cart_view.xml",
        

    ],
    "demo": [
        "data/demo_product.xml",
    ],

    'images': ['static/description/icon.png'],

    "installable": True,
    "application": True,

}