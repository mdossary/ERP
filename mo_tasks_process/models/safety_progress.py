from odoo import fields, models, api,_


class SafetyProgress(models.Model):
    _name = 'safety.progress'
    _description = 'Safety  Progress Management'

    """
    Header Fields : 
    Point one to four ***
    """

    task_id = fields.Many2one(
        comodel_name='project.task',
        string='Task',
        required=False)

    name = fields.Char()

    unit_name = fields.Char(
        string='Name of the Unit (Zone)',
        required=False)

    incident_date = fields.Date(
        string='Date of the the incident',
        default=fields.Date.today(),
        required=False)
    location = fields.Float(
        string='Location',
        required=False)
    time_incident = fields.Float(
        string='Time of the incident',
        required=False)

    equipment_tag = fields.Char(
        string='Equipment Tag',
        required=False)

    type_incident = fields.Selection(
        string='Type or Category of incident',
        selection=[('employee', 'Company Employee'),
                   ('contractor', 'Contractor'), ],
        required=False, )

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('safety.progress') or _('New')
        return super(SafetyProgress, self).create(vals)

    """
       Table Fields : 
       Point number Five ***
       """

    safety_table_ids = fields.Many2one(
        comodel_name='safety.table.management',
        string='Table Lines',
        required=False)

    """
    body Contents :::
    """

    spill_duration = fields.Float(
        string='Duration of spill/Release',
        required=False)

    if_spill = fields.Selection(
        string='Spill/Release Type',
        selection=[('indoor', 'Indoor'),
                   ('outdoor', 'Outdoor'), ],
        required=False, )

    name_chemical = fields.Char(
        string='Name of Chemical(s) and composition',
        required=False)

    qty = fields.Float(
        string='Quantity of spill/Release',
        required=False)



