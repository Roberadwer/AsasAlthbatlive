# -*- coding: utf-8 -*-
{
    'name': "Employee termination",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Ahmed Saber",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr_contract', 'account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/termination_approval_group.xml',
        'views/hr_termination.xml',
        'views/hr_contract.xml',
        'views/account_move.xml',
        'reports/termination_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
