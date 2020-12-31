# -*- coding: utf-8 -*-
{
    'name': "除蟲任務（升級版）",

    'summary': """
        除蟲任務的工作處理流程
    """,

    'description': """
        1.增加簡易的工作流程處理功能 \n
        2.增加看板功能 \n
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'bug_manage'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/bugs.adv.xml',
        'views/bugs_stage.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
