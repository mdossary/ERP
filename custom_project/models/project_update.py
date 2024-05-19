from odoo import api, fields, models


class ProjectUpdate(models.Model):
    _inherit = 'project.update'



    project_name = fields.Char(
        string='Project Name',
        compute='_compute_project_name',
        required=False)


    report_no = fields.Integer(
        string='Report No',
        required=False)

    overall_status = fields.Text(
        string="Overall Status",
        required=False)

    safety = fields.Text(
        string="Safety",
        required=False)

    end_date = fields.Date(
        string='End Date',
        required=False)

    task_and_activities = fields.Text(
        string="Task And Activities",
        required=False)

    challenges = fields.Text(
        string="Challenges",
        required=False)

    any_other_items = fields.Text(
        string="Any Other Items",
        required=False)

    s_curve = fields.Binary(string="S-Curve")

    @api.onchange('project_id')
    def _compute_project_name(self):
        if self.project_id:
            if self.project_id.name:
                self.project_name = self.project_id.name
        else:
            self.project_name = ''
