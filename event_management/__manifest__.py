{
    "name":"event_management",
    "version":"1.0",
    "depends":["base","mail"],
    "license": 'LGPL-3',
    "author":"Vivek Panjwani",
    "data":[
        "data/email_template_registration.xml",
        "security/event_security.xml",
        "security/ir.model.access.csv",
        

        "views/event_registration.xml",
        "views/event_organizer.xml",
        "views/event_attendee.xml",
        "views/event_views.xml",


        "wizard/registration_report.xml",
        ],
    "installable":True,
    "application":True,
    "summary":"Event Management",
    "description":"Here You can manage the events",
}
