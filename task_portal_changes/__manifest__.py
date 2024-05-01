# -*- coding: utf-8 -*-
{
    'name': "Changes in Portal Tasks",
    'summary': """
        According To BA in this module we Develop Portal >> Task 
        And Make Some Changes in tree view and Form View""",
    'author': "Mo Esam",
    'category': 'portal',
    'version': '16.0.0.1',
    # any module necessary for this one to work correctly
    'depends': ['portal', 'project', 'hr_timesheet'],
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/project_portal_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
