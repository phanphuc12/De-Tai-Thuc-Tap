from odoo import api, fields, models


class Department(models.Model):
    _name = "hr.department"
    _description = 'Department'
    _inherit = 'hr.department'

    members = fields.Many2many('hr.employee', string="Member", required=True)
