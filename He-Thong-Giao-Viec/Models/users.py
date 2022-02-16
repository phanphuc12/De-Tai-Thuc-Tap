from odoo import api, fields, models, tools, _


class Users(models.Model):
    _name = "res.users"
    _inherit = "res.users"

    test = fields.Char('test')
