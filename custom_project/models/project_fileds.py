from odoo import fields, models, api, _
from datetime import datetime, timedelta


class ProjectTask(models.Model):
    _inherit = 'project.task'
    

    mo_duration_aot = fields.Float(
        string='Duration (D)',
        compute='_get_mo_duration',
        required=False)
    
    mo_duration_aot_day = fields.Float(
        string='Duration AOT (D)',
        compute='_get_mo_duration_day',
        required=False)
    
    
    mo_star =fields.Selection(
        string='Priorty',
        selection=[('normal', 'Normal'),
                   ('low', 'Low'),('high', 'High'),('v_high', 'Very High') ],
        required=False)
    

    mo_wt = fields.Float(
        string='WT',
        required=False)
    
    mo_wt_per_day = fields.Float(
        string='WT/ Day %',
        compute='_get_wt_per_day',
        required=False)
    
   
    
    mo_item_actual_progress_aot = fields.Float(
        string='Actual Progress %',
        required=False)

    mo_planned_progress = fields.Float(
        string='Planned Progress AOT %',
        compute='_get_planned_aot_rate',
        required=False)

    mo_difference = fields.Float(
        string='Difference %',
        compute='_return_different',
        required=False)
    
    
    @api.depends('progress','mo_duration_aot',)
    def _get_mo_duration_day(self):
        for rec in self:
            if rec.planned_date_begin:
                if rec.progress <= 100 :
                    rec.mo_duration_aot_day = (fields.Datetime.today() - rec.planned_date_begin).days + 1
                else:
                    rec.mo_duration_aot_day = rec.mo_duration_aot
            else: 
                rec.mo_duration_aot_day = 0
    
    
    @api.depends('mo_duration_aot','mo_wt')
    def _get_wt_per_day(self):
        for rec in self:
            if rec.mo_duration_aot == 0 :
                rec.mo_wt_per_day = 0
            else:
                rec.mo_wt_per_day= (rec.mo_wt / rec.mo_duration_aot)
    

    @api.depends('planned_date_begin', 'planned_date_end')
    def _get_mo_duration(self):
        for rec in self:
            if rec.planned_date_begin and rec.planned_date_end:
                start = rec.planned_date_begin
                end =rec.planned_date_end
                duration = (end - start).days + 1
                rec.mo_duration_aot = duration
            else:
                rec.mo_duration_aot = 0.0
                
    @api.depends(
        'mo_duration_aot_day',
        'mo_duration_aot',
        'mo_wt','mo_wt_per_day'
        )
    def _get_planned_aot_rate(self):
        for r in self:
            totalplanned = 0
            c = 0
            if r.mo_duration_aot_day <= r.mo_duration_aot :
                totalplanned = (r.mo_duration_aot_day * r.mo_wt)
                if totalplanned < 0 :
                    r.mo_planned_progress= 0
                else:
                    r.mo_planned_progress = totalplanned
            else:
                c = r.mo_duration_aot * r.mo_wt_per_day
                r.mo_planned_progress = c
                
    @api.depends('mo_item_actual_progress_aot','mo_planned_progress')
    def _return_different(self):
        for rec in self:
            rec.mo_difference = rec.mo_item_actual_progress_aot - rec.mo_planned_progress
        

    