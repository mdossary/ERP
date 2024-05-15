from odoo import fields, models, api
from datetime import datetime


class Project(models.Model):
    _inherit = 'project.project'

    target_tasks = fields.One2many(comodel_name='project.task', inverse_name='project_id')

    count_tasks = fields.Many2many(
        comodel_name='project.task',
        domain="[('id', 'in', target_tasks)]",
        string='Target Tasks')
        

    mo_planned_wt = fields.Float(
        string='Planned WT',
        compute='return_actual_planned_wt',
        required=False)

    mo_actual_wt = fields.Float(
        string='Actual WT',
        compute='return_actual_planned_wt',
        required=False)

    def return_actual_planned_wt(self):
        for res in self:
            if res.count_tasks:
                planned = []
                actual = []
                for rec in res.count_tasks:
                    actual.append(rec.x_studio_item_actual_progress_aot_)
                    planned.append(rec.x_studio_planned_progress_)
                plan_total = "%.2f" % sum(planned)
                actual_total = "%.2f" % sum(actual)
                res.mo_actual_wt = actual_total
                res.mo_planned_wt = plan_total
            else:
                res.mo_actual_wt = 0
                res.mo_planned_wt = 0

    def return_actual_planned_wt(self):
        for rec in self:
            actual = 0
            planned = 0
            for task in rec.task_ids:
                if not task.child_ids:
                    actual += task.all_wt_parent
                    planned += task.all_planned
            output_actual = "%.2f" % actual
            output_planned = "%.2f" % planned
            rec.mo_planned_wt = output_actual
            rec.mo_actual_wt = output_planned


class ReportTasks(models.Model):
    _inherit = 'project.update'

    def without_round(self, number):
        output = "%.2f" % number
        return output

    def _get_subtasks_rate(self, parent):
        for clac in self:
            my_list = []
            child_ids = parent.child_ids
            for ch in child_ids:
                done_process_lines = ch.process_line_ids.filtered(lambda l: l.state == 'done')
                progress_rate = sum(done_process_lines.mapped('rate'))
                my_list.append(progress_rate)
            parent_rate = sum(my_list) / len(child_ids)
            return round(parent_rate, 2)

    def sort_by_subtask(self, tasks):
        new_res = []
        # Sort tasks by parent ID
        sorted_tasks = sorted(tasks, key=lambda x: x.name)
        for line in sorted_tasks:
            date_end = line.planned_date_end
            done_process_lines = line.process_line_ids.filtered(lambda l: l.state == 'done')
            new_res.append({
                'condition': line.child_ids,
                'parent': line.name,
                'progress': round(line.tree_progress, 2),
                'planned_date_end': line.date_deadline,
                'x_studio_n_actual': self.without_round(line.all_wt_parent),
                'x_studio_n_planned': self.without_round(line.all_planned)
            })
        return new_res

    def actual_header(self, project):
        actual = []
        for po in project.count_tasks:
            actual.append(po.x_studio_item_actual_progress_aot_)
        result = sum(actual) * 100
        output = "%.2f" % result
        return result

    def planned_header(self, project):
        planned = []
        for po in project.count_tasks:
            planned.append(po.x_studio_planned_progress_)
        result = sum(planned) * 100
        output = "%.2f" % result
        return result
