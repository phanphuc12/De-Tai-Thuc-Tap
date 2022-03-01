from odoo import fields, models, api, _


class TopicCategories(models.Model):
    _name = "topic.category"

    name = fields.Char(string="Topic Name", required=True)
    department = fields.Many2one('hr.department', string="Department", required=True)
    description = fields.Text(string="Description")
