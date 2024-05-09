from odoo import fields, models, api
from datetime import datetime


class Project(models.Model):
    _inherit = 'project.project'

    count_tasks = fields.Many2many(
        comodel_name='project.task',
        domain="[('id', 'in', task_ids)]",
        string='Target Tasks')


class ReportTasks(models.Model):
    _inherit = 'project.update'

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
                'x_studio_n_actual': round(line.x_studio_n_actual, 2),
                'x_studio_n_planned': round(line.x_studio_n_planned, 2)
            })
        return new_res

    def actual_header(self, project):
        actual = []
        for po in project.count_tasks:
            actual.append(po.x_studio_item_actual_progress_aot_)
        result = sum(actual) * 100
        return round(result, 2)

    def planned_header(self, project):
        planned = []
        for po in project.count_tasks:
            planned.append(po.x_studio_planned_progress_)
        result = sum(planned) * 100
        return round(result, 2)
