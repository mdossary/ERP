# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': ' Tasks Process',
    'summary': 'Project Tasks Workflow',
    "license": "OPL-1",
    'version': '16.0.0.2',
    'category': 'Project',
    'author': 'Mohamed Isam',
    'depends': ['project', 'hr_timesheet','studio_customization','project_enterprise'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/sequence_data.xml',
        'views/tasks_process.xml',
        'views/report_template.xml',
        # 'views/safety_view_form.xml',
    ],
    'assets': {
        'web.report_assets_pdf': [
            '/mo_tasks_process/static/src/scss/progress_style.css',
        ],
    },
    'application': True,
    'installable': True,
}
