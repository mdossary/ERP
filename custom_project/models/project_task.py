from odoo import fields, models, api, _


class ProjectTask(models.Model):
    _inherit = 'project.task'

    action_count = fields.Integer(
        string='Action Items',
        compute='_compute_action_item_mom'

    )
    mom_count = fields.Integer(
        string='MoM',
        compute='_compute_action_item_mom'

    )
    sub_tasks_count = fields.Integer(
        string='Sub-Tasks',
        compute='_compute_action_item_mom'

    )



    def _compute_action_item_mom(self):
        for rec in self:
            items_count = self.env['action.items'].search_count([('project_task', '=', rec.id)])
            mom_count = self.env['mom.mom'].search_count([('project_task', '=', rec.id)])
            # sub_tasks_count = self.env['project.task'].search_count([('')])
            rec.action_count = items_count
            rec.mom_count = mom_count
            # rec.sub_tasks_count =sub_tasks_count




    def action_item_count(self):
        for rec in self:
            return {
                "type": "ir.actions.act_window",
                "res_model": "action.items",
                "views": [[False, "tree"]],
                "context": {
                    'default_project_task': rec.id,
                },
            }

    def action_mom(self):
        for rec in self:
            return {
                "type": "ir.actions.act_window",
                "res_model": "mom.mom",
                "views": [[False, "tree"]],
                "context": {
                    'default_project_task': rec.id,
                },
            }


class ProjectProject(models.Model):
    _inherit = 'project.project'

    action_count = fields.Integer(
        string='Action Items',
        compute='_compute_action_item_mom'

    )
    mom_count = fields.Integer(
        string='MoM',
        compute='_compute_action_item_mom'

    )


    company_id = fields.Many2one(comodel_name="res.company",string="Company")

    project_logo = fields.Binary(string="Project Logo")

    report_image = fields.Binary(string="Report Images")

    action_item_obj = fields.One2many(comodel_name='action.items',inverse_name='project',string='Action Items')

    mom_obj = fields.One2many(comodel_name='mom.mom',inverse_name='project',string='MOM')




    def _compute_action_item_mom(self):
        for rec in self:
            items_count = self.env['action.items'].search_count([('project', '=', rec.id)])
            mom_count = self.env['mom.mom'].search_count([('project', '=', rec.id)])
            rec.action_count = items_count
            rec.mom_count = mom_count





    def action_item_count(self):
        for rec in self:
            return {
                "type": "ir.actions.act_window",
                "res_model": "action.items",
                "views": [[False, "tree"]],
                "context": {
                    'default_project': rec.id,
                },
            }

    def action_mom(self):
        for rec in self:
            return {
                "name": _("Sub-Tasks"),
                "type": "ir.actions.act_window",
                "res_model": "mom.mom",
                "views": [[False, "tree"]],
                "context": {
                    'default_project': rec.id,
                },
            }
        
        


