from odoo import fields, models, api


class ActionItemTag(models.Model):
    _name = 'action.items.tags'
    _description = 'Description'

    name = fields.Char()

    color = fields.Integer(
        string='Color',
        required=False)

