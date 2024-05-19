from odoo import fields, models, api, _


class ActionItems(models.Model):
    _name = 'action.items'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Description'

    seq = fields.Char()

    due_date = fields.Date(
        string='Due Date',
        required=False,
        tracking=True)
    

    name = fields.Char(
        string='Name',
        required=False,
        translate=True,
        tracking=True)

    description = fields.Char(
        string='Description',
        required=False,
        tracking=True)

    project = fields.Many2one(
        comodel_name='project.project',
        string='Project',
        required=False,
        tracking=True)

    project_task = fields.Many2one(
        comodel_name='project.task',
        string='Task',
        required=False,
        tracking=True)

    mom = fields.Many2one(
        comodel_name='mom.mom',
        string='MOM',
        required=False,
        tracking=True)

    action_party = fields.Many2many(
        comodel_name='action.items.tags',
        string='Action Party',
        tracking=True)

    company = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        required=False,
        tracking=True)

    remark = fields.Text(
        string="Remark",
        required=False,
        tracking=True)








