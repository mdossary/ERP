from odoo import fields, models, api


class RoundTask(models.Model):
    _inherit = 'project.task'

    def get_round_values(self, value):
        round_value = round(value, 2)
        return round_value

