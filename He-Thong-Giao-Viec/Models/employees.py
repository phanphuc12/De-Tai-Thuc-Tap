from odoo import api, fields, models, tools, _


class HrEmployeePrivate(models.Model):
    _name = "hr.employee"
    _inherit = "hr.employee"

    family_lines = fields.One2many('hr.family', 'family_id')


class family(models.Model):
    _name = 'hr.family'

    name = fields.Text("Full Name")
    day_of_birth = fields.Date("Date Of Birth")
    nationality = fields.Many2one('res.country', string='Lationality')
    ethnic_group = fields.Char("Ethnic Group")
    permanent_address = fields.Text("Permanent Address")
    family_id = fields.Many2one('hr.employee')
