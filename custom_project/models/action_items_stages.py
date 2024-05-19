from odoo import fields, models, api


class ActionItemStages(models.Model):
    _name = 'action.items.stages'
    _description = 'Description'

    name = fields.Char()

    stage_name = fields.Char(
        string='Stage Name',
        required=False)

    user_id = fields.Char(
        string='User_id',
        readonly=True,
        default=lambda self: self.env.user.name,
        required=False)