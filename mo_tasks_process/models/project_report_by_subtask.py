from odoo import fields, models, api
from datetime import datetime


class ReportTasks(models.Model):
    _inherit = 'project.update'

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
                'progress': round(sum(done_process_lines.mapped('rate')), 2),
                'planned_date_end': date_end.date() if date_end else False,
                'x_studio_n_actual': round(line.x_studio_n_actual, 2),
                'x_studio_n_planned': round(line.x_studio_n_planned, 2)
            })
        return new_res
