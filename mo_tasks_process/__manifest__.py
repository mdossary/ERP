# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': ' Tasks Process',
    'summary': 'Project Tasks Workflow',
    "license": "OPL-1",
    'category': 'Project',
    'author': 'Mohamed Isam',
    'depends': ['project', 'hr_timesheet'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        # 'data/sequence_data.xml',
        'views/tasks_process.xml',
        # 'views/safety_view_form.xml',
    ],
    'application': True,
    'installable': True,
}
