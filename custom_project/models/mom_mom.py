from odoo import fields, models, api,_


class MomMom(models.Model):
    _name = 'mom.mom'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Description'

    name = fields.Char(string="Meeting Reference")

    meeting_date = fields.Date(
        string='Meeting Date',
        required=False,
        tracking = True)

    time = fields.Char(
        string='Time',
        required=False,
        tracking=True)

    location = fields.Char(
        string='Location',
        required=False,
        tracking=True)

    attendees = fields.Many2many(
        comodel_name='res.partner',
        string='Attendees',
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

    company = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        required=False,
        tracking=True)

    agenda = fields.Text(
        string="Agenda",
        required=False,
        tracking = True)

    discussion_summary = fields.Text(
        string="Discussion Summary",
        required=False,
        tracking=True)

    type_down = fields.Text(
        string="Type Down",
        required=False,
        tracking=True)

    action_item_ids = fields.One2many(
        comodel_name='action.items',
        inverse_name='mom',
        string='Action Items',
        required=False,
        tracking=True)

    items_count = fields.Integer(
        string='Appointment Count',
        compute='_compute_item_count')
    
    attachment = fields.Char(
        string='Attachment',
        required=False)


    def _compute_item_count(self):
        for rec in self:
            items_count = self.env['action.items'].search_count([('mom', '=', rec.id)])
            rec.items_count = items_count



    def action_item_count(self):
        for rec in self:
            target = self.env['action.items'].search_count([('mom', '=', rec.id)])

        return {
            "type": "ir.actions.act_window",
            "res_model": "action.items",
            "views": [[False, "tree"]],
            "domain": [("mom", "in", rec.name)],
            "name": _("Action Items"),
        }
    






