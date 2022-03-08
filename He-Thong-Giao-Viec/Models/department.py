from odoo import api, fields, models, _


class Department(models.Model):
    _name = "hr.department"
    _description = 'Department'
    _inherit = 'hr.department'

    members = fields.Many2many('hr.employee', string="Member", required=True)
    name_seq = fields.Char(string='ID', required=True, copy=False, readonly=True, index=True,
                           default=lambda self: _('New'))

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '%s - %s' % (('[' + rec.name_seq + ']'), rec.name)))
        return res

    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('department.s.sequence') or _('New')
        result = super(Department, self).create(vals)
        return result
