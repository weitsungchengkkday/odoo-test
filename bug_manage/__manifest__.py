# -*- coding: utf-8 -*-
{
    'name': "bug_manage",
    'summary': """sSSSSs""",
    'description': """
        pPPPPp
        pPPPPp
        pPPPPp
    """,
    'author': "William Cheng",
    'website': "www.weitsungcheng.com",

    'category': "Bug Manage",

    'version': "0.4",

    'depends': ['base', 'kk_restful'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/bug_list.xml',
        'views/bug_form.xml',
        'views/bug_search.xml',
        'views/follower_form.xml',
        'views/follower_tree.xml',
        'views/menu.xml',
        'views/bugs_template.xml',
        'views/bugs_details_page.xml',
  #      'views/res_config_settings_views.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml'
    ],
}
