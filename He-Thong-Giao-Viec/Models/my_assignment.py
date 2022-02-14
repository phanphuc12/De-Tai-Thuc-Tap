from odoo import fields, models, api, _


class MyAssignment(models.Model):
    _name = "my.assignment"
    _description = "My Assignment"

    department = fields.Many2one('hr.department', string="Department", required=True)
    employee = fields.Many2one('hr.employee', string='Employee', required=True)
    deadline = fields.Datetime(string='Deadline', required=True)
    description = fields.Text(string='Description')
    name_seq = fields.Char(string='ID', required=True, copy=False, readonly=True, index=True,
                           default=lambda self: _('New'))
