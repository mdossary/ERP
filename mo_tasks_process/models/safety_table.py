from odoo import fields, models, api


class ModelName(models.Model):
    _name = 'safety.table.management'
    _description = 'Safety Table Checklist'

    type_of_safety = fields.Selection(
        string='Safety Category',
        selection=[('occupational', 'Occupational Injury'),
                   ('property', 'Property Damage'),
                   ('fire', 'Fire/Explosion'),
                   ],
        required=False, )

    if_occupational = fields.Selection(
        string='Occupational Injury Sub',
        selection=[('fatality', 'Fatality'), ('lost', 'Lost Workday'), ('restricted', 'Restricted Workday'),
                   ('medical', 'Medical Treatment'), ('aid', 'First Aid'), ],
        required=False, )

    process_safety = fields.Selection(
        string='Process Safety',
        selection=[
            ('tier_1', 'Tier 1'),
            ('tier_2', 'Tier 2'),
            ('tier_3', 'Tier 3')],
        required=False, )

    health = fields.Selection(
        string='Health Categories',
        selection=[('occupational', 'Occupational illness')],
        required=False, )

    if_illness = fields.Selection(
        string='Occupational illness Sub',
        selection=[('fatality', 'Fatality'), ('lost', 'Lost Workday'), ('restricted', 'Restricted Workday'),
                   ('medical', 'Medical Treatment'), ('aid', 'First Aid'), ],
        required=False, )

    enviro = fields.Selection(
        string='Environment',
        selection=[
            ('hazardous', 'Hazardous Chemicals/Substance'),
            ('not_hazardous', 'Non Hazardous Chemicals/Substance'),
            ('vent', 'Vent/Stack Emission'),
            ('sea', 'Sea/Canal/River/Storm/Rainwater'),
            ('waste', 'Waste Water'),
            ('ground', 'Ground Water /Soil'),
            ('smoky', 'Smoky Flaring'),
            ('noise', 'Noise'),
            ('radio', 'Radioactive Material'),
        ],
        required=False, )

    security = fields.Selection(
        string='Security',
        selection=[('information', 'Information'),
                   ('electronic', 'Electronic System'),
                   ('personnel', 'Personnel/Physical'),
                   ],
        required=False, )


