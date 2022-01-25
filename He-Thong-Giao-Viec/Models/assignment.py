from odoo import api, fields, models, _


class assignment(models.Model):
    _name = "assignment.s"
    _inherit = ["mail.thread"]

    name = fields.Char(string='name')
    age = fields.Char("age")
    name_seq = fields.Char(string='ID', required=True, copy=False, readonly=True, index=True,
                           default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('assignment.s.sequence') or _('New')
        result = super(assignment, self).create(vals)
        return result

