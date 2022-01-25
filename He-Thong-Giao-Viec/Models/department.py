from odoo import api, fields, models


class Department(models.Model):
    _name = "hr.department"
    _description = 'Department'
    _inherit = 'hr.department'

    test = fields.Text(string="test1")
