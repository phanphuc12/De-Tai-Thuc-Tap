from odoo import api, fields, models, _


class Rating(models.Model):
    _name = "employee.rating"

    name = fields.Char(string='Name')
    name_seq = fields.Char(string='ID', required=True, copy=False, readonly=True, index=True,
                           default=lambda self: _('New'))
    employee_rate = fields.Char(string='Rating')
