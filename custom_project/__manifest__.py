# -*- coding: utf-8 -*-

{
    'name': 'Gait Custom Project',
    'version': '16.0.1.1.0',
    'category': '',
    'summary': """
        Transfer Project Studio Customization To This Module
        
    """,
    'author': 'Ahmed Abdu',
    'website': '',
    'depends': ['base', 'project', 'mail','project_enterprise'],
    'data': [
        'security/ir.model.access.csv',
        'views/mom_mom.xml',
        'views/action_items.xml',
        'views/action_items_tags.xml',
        'views/project_task.xml',
        'views/project_task_fields.xml',
        'views/project_update.xml',
    ],

    'assets': {
        'web.report_assets_pdf': [
            '/custom_project/static/src/css/round.css',
        ],
    },

    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'AGPL-3',

}