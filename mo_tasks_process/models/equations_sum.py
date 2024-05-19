from odoo import fields, models, api


class ProjectTasksForm(models.Model):
    _inherit = 'project.task'

    """
    Fields Description : 
    
    process_line_ids >>>>>>        O2m To show Progress Tab.
    tracking_log >>>>>>            To Pass Tab Details To Parent Project.task.
    progress_widget >>>>>>         This is A Widget Bar To Show O2M Progress Rate.
    process_widget_flag >>>>>>     Hook to skip computed Fields in tree view.
    parent_show >>>>>>             Flag To Hide Progress Tab When It's Parent Task.
    parent_flag >>>>>>              Hook also yo skip un stored Field parent_show.
    
    """

    process_line_ids = fields.One2many(
        comodel_name='mo.process.workflow',
        inverse_name='task_id',
        string='Process Line',
        required=False)

    tracking_log = fields.Text(
        string="Progress Details",
        tracking=True,
        required=False)

    progress_widget = fields.Float(
        string='Progress',
        compute='_get_progress_widget',
        required=False)

    process_widget_flag = fields.Float(
        string='Progress',
        compute='_set_default_progress',
        required=False)

    tree_progress = fields.Float(
        string='Progress',
        required=False)

    parent_show = fields.Boolean(
        string='Parent Show',
        compute='_get_parent_show',
        required=False)

    parent_flag = fields.Boolean(
        string='Parent Show',
        required=False)

    all_progress = fields.Float(
        string='All Progress',
        compute='set_all_progress',
        required=False)

    all_wt_parent = fields.Float(
        string='All WT',
        compute='set_all_progress_wt',
        required=False
    )
    all_planned = fields.Float(
        string='All Planned',
        compute='set_all_progress_wt',
        required=False
    )
    
    #Cron Job Function :

    def task_studio_cron(self): 
        for rec in self:
            tasks = rec.search([])
            for r in tasks:
                r._get_mo_duration_day()
                r._get_wt_per_day()
                r._get_mo_duration()
                r._get_planned_aot_rate()
                r._return_different()
                
           
    def _get_subtasks_rate(self, parent):
        """
        This Function : Receive Parent id and then return the subtasks progress Rate
        Eq: parent_rate = sum(Subtasks Rates) / count(subtasks)
        """
        for clac in self:
            my_list = []
            child_ids = parent.child_ids
            for ch in child_ids:
                done_process_lines = ch.process_line_ids.filtered(lambda l: l.state == 'done')
                progress_rate = sum(done_process_lines.mapped('rate'))
                my_list.append(progress_rate)
            parent_rate = sum(my_list) / len(child_ids)
            return parent_rate

    @api.depends('progress_widget')
    def set_all_progress(self):
        for record in self:
            my_list = []
            count = 0
            for ch in record.child_ids:
                count = count + 1
                my_list.append(ch.process_widget_flag)
            record.all_progress = sum(my_list) / count if sum(my_list) > 0 else sum(my_list)

    def _set_default_progress(self):
        """
            This Function : Computation Method For process_widget_flag
                                                                        """
        for rec in self:
            if not rec.child_ids:
                rate = rec.process_line_ids.filtered(lambda line: line.state == 'done').mapped('rate')
                action = sum(rate)
                rec.process_widget_flag = action
                rec.write({'tree_progress': action})
            else:
                my_list = []
                count = 0
                for ch in rec.child_ids:
                    count = count + 1
                    my_list.append(ch.process_widget_flag)
                rate = sum(my_list) / count if sum(my_list) > 0 else sum(my_list)
                rec.update({'process_widget_flag': rate})
                rec.update({'tree_progress': rate})
                print('nnnnnnnnnnnnnnnnnnnnnnnnnnnn', rec.process_widget_flag)

    def _get_subtasks_wt(self, parent):
        """
        This Function :
        """
        for wt in self:
            my_list = []
            child_ids = parent.child_ids
            for ch in child_ids:
                subtask_weight = ch.mo_wt
                aot_rate = ch.mo_item_actual_progress_aot
                plan_rate = ch.mo_planned_progress
                my_list.append({
                    'subtask_weight': subtask_weight,
                    'aot': aot_rate,
                    'plan': plan_rate
                })
            return my_list

    @api.depends('child_ids')
    def _get_parent_show(self):
        """
        This Function: Return The Total pARENT Of Values :
         -WT
         -AOT
         -pLAN

        """
        for rec in self:
            if rec.child_ids:
                rec.parent_show = False
                items = self._get_subtasks_wt(rec)
                wt = round(sum(item['subtask_weight'] for item in items), 2)
                aot = sum(item['aot'] for item in items)
                plan = round(sum(item['plan'] for item in items), 2)
                rec.update({
                    'parent_flag': False,
                    'mo_wt': wt,
                    'mo_item_actual_progress_aot': aot,
                    'mo_planned_progress': plan
                })
            else:
                rec.parent_show = True
                rec.write({'parent_flag': True})

    @api.depends('mo_wt', 'process_line_ids')
    def _get_progress_widget(self):
        """
        This Function : Calculate The progress Widget
        Please Note That This Filed :progress_widget dOES NOT Store To DB
        """
        for widget in self:
            if not widget.child_ids:
                my_list = []
                line_ids = self.process_line_ids
                for line in line_ids:
                    my_list.append(line.rate) if line.state == 'done' else 0
                widget.progress_widget = sum(my_list)
            else:
                result = self._get_subtasks_rate(widget)
                widget.progress_widget = result

    def set_all_progress_wt(self):
        for record in self:
            my_list = []
            plan = []
            if not record.child_ids:
                record.all_wt_parent = record.mo_item_actual_progress_aot * 100 if record.mo_item_actual_progress_aot > 0 else record.mo_item_actual_progress_aot
                record.all_planned = record.mo_planned_progress * 100 if record.mo_planned_progress > 0 else record.mo_planned_progress
            else:
                for ch in record.child_ids:
                    my_list.append(ch.mo_item_actual_progress_aot)
                    plan.append(ch.mo_planned_progress)
                record.all_wt_parent = sum(my_list) * 100 if sum(my_list) > 0 else sum(my_list)
                record.all_planned = sum(plan) * 100 if sum(plan) > 0 else sum(plan)
