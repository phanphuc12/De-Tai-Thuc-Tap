from odoo import fields, models, api, _


class TopicCategories(models.Model):
    _name = "topic.category"

    name = fields.Char(string="Topic Name", required=True)
    department = fields.Many2one('hr.department', string="Department", required=True)
    description = fields.Text(string="Description")
    type = fields.Selection([
        ('1', 'Assignment'),
        ('2', 'Assistance')
    ], string="Type", default="1")
