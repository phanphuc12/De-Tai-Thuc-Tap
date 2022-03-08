from odoo import api, fields, models, tools, _


class HrEmployeePrivate(models.Model):
    _name = "hr.employee"
    _inherit = "hr.employee"

    family_lines = fields.One2many('hr.family', 'family_id')
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
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('employee.s.sequence') or _('New')
        result = super(HrEmployeePrivate, self).create(vals)
        return result


class Family(models.Model):
    _name = 'hr.family'

    name = fields.Text("Full Name")
    day_of_birth = fields.Date("Date Of Birth")
    nationality = fields.Many2one('res.country', string='Nationality')
    ethnic_group = fields.Char("Ethnic Group")
    permanent_address = fields.Text("Permanent Address")
    family_id = fields.Many2one('hr.employee')
