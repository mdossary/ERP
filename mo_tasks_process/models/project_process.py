from odoo import fields, models, tools, api, _
from odoo.exceptions import ValidationError

import datetime
from dateutil.relativedelta import relativedelta


class MoTaskProcess(models.Model):
    _name = 'mo.processs.workflow'

    @api.model
    def create(self, values):
        if self.env.user.has_group('mo_tasks_process.mo_group_task_project_manager_one'):
            raise ValidationError("Only users are allowed to add lines.")
        return super(MoTaskProcess, self).create(values)

    name = fields.Char()

    date_process = fields.Date(
        string='Date',
        default=fields.Date.today(),
        required=False)

    user_process = fields.Many2one(
        comodel_name='res.users',
        string='Current User',
        default=lambda self: self.env.user,
        required=True)

    manager_process = fields.Many2one(
        comodel_name='res.users',
        string='Manager Name',
        compute='return_manager_id',
        required=False)

    user_note = fields.Text(
        string="User Description",
        required=True)

    user_note_flag = fields.Text(
        string="User Description",
        compute='change_log_text',
        required=True)

    manager_note = fields.Text(
        string="Manager Description",
        required=False)

    action_click = fields.Boolean(
        string='Action Click',
        required=False)

    readonly_trigger = fields.Boolean(
        string='Readonly Line',
        required=False)

    rate = fields.Integer(
        string='Rate %',
        required=False)

    task_id = fields.Many2one(
        comodel_name='project.tassk',
        string='Task',
        required=False)

    state = fields.Selection(
        string='Status',
        selection=[('done', 'Approved'),
                   ('not', 'Rejected'), ],
        required=False)

    progress_widget = fields.Float(
        string='Progress',
        related='task_id.progress',
        required=False)

    if_user = fields.Boolean(
        string='If User',
        compute='readonly_manager_user',
        required=False)

    if_manager = fields.Boolean(
        string='If Manager',
        required=False)
    
    if_manager_flag = fields.Boolean(
        string='If Manager',
        compute='note_manager_readonly',
        required=False)

    @api.depends('user_process', 'manager_process')
    def readonly_manager_user(self):
        for rec in self:
            supervisor = rec.user_process
            manager = rec.manager_process
            if supervisor == self.env.user:
                rec.if_user = False
            else:
                rec.if_user = True
            if manager == self.env.user:
                rec.if_manager = False
            else:
                rec.if_manager = True
                
    def note_manager_readonly(self):
        for rec in self:
            if self.env.user.has_group('mo_tasks_process.mo_group_task_project_manager_one'):
                rec.write({'if_manager_flag':True})
            else:
                rec.write({'if_manager_flag':False})
                

    @api.depends('user_note')
    def change_log_text(self):
        for rec in self:
            body = "User : %s Add Progress in Date %s with Description %s ,and Progress = %s " \
                   % (rec.user_process.name, rec.date_process, rec.user_note, rec.rate)
            if rec.user_note:
                rec.task_id.write({'tracking_log': "New Progress == :"})
                rec.write({'user_note_flag': body})
                rec.task_id.write({'tracking_log': body})
            else:
                rec.write({'user_note_flag': False})

    def return_manager_id(self):
        for rec in self:
            rec.manager_process = self.env.user

    def _pass_value_to_log(self):
        for rec in self:
            body = "User : %s Add Progress in Date %s with Description %s , Manager Description : %s and Progress = %s " \
                   ", Status : %s" \
                   % (rec.user_process.name, rec.date_process, rec.user_note, rec.manager_note, rec.rate,
                      "Approved" if rec.state == 'done' else "Rejected")
            rec.task_id.write({'tracking_log': "New Progress == :"})
            rec.task_id.write({'tracking_log': body})

    def appear_const(self):
        raise ValidationError(_("You Can Not Use This Percent it the actual or WT will be more than 100 %"))

    def check_progress_limitation(self, rate):
        acc = self.task_id
        line_rate = rate / 100
        wt = self.task_id.x_studio_weight
        check = acc + (line_rate * wt)
        total_rate = sum(self.task_id.process_line_ids.filtered(lambda line: line.state == 'done').mapped('rate'))
        if total_rate > 100 or rate + total_rate > 100:
            self.appear_const()
        else:
            return check

    def process_timesheet(self):
        for rec in self:
            check = self.check_progress_limitation(rec.rate)
            rec.task_id.write({'x_studio_item_actual_progress_aot_': check})
            rec.write({'action_click': True})
            rec.write({'readonly_trigger': True})
            rec.write({'state': 'done'})
            self._pass_value_to_log()

    def reject_process(self):
        for reject in self:
            reject.write({'action_click': True})
            reject.write({'readonly_trigger': True})
            reject.write({'state': 'not'})
            self._pass_value_to_log()
            
    
            
