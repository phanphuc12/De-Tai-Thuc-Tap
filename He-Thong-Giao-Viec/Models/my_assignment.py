from odoo import fields, models, api, _


class MyAssignment(models.Model):
    _name = "my.assignment"
    _description = "My Assignment"

    department = fields.Many2one('hr.department', string="Department")
    employee = fields.Many2one('hr.employee', string='Employee')
    description = fields.Text(string='Description')
    deadline = fields.Datetime(string='Deadline')
    name_seq = fields.Char(string='ID')
