from odoo import api, fields, models, tools, _


class HrEmployeePrivate(models.Model):
    _name = "hr.employee"
    _inherit = "hr.employee"

    family_lines = fields.One2many('hr.family', 'family_id')
    name_seq = fields.Char(string='ID', required=True, copy=False, readonly=True, index=True,
                           default=lambda self: _('New'))
    employee_rate = fields.Char('Employee Rate Final', compute='rating_employee')

    def send_employee(self):
        vals = {
            'name_seq': self.name_seq,
            'name': self.name,
            'employee_rate': self.employee_rate,
        }
        self.env['employee.rating'].create(vals)

    def write(self, vals):
        ch = super(HrEmployeePrivate, self).write(vals)
        for rec in self:
            self.env['employee.rating'].search([('name_seq', '=', rec.name_seq)]).write({
                'name': rec.name,
                'employee_rate': rec.employee_rate,
            })
        return ch

    def rating_employee(self):
        for rate in self:
            total_bad_rating = self.env['my.assignment'].search_count(
                [('rating', '=', 'bad'), ('employee', '=', rate.name)])
            total_good_rating = self.env['my.assignment'].search_count(
                [('rating', '=', 'good'), ('employee', '=', rate.name)])
            total_perfect_rating = self.env['my.assignment'].search_count(
                [('rating', '=', 'perfect'), ('employee', '=', rate.name)])
            if (total_bad_rating + total_good_rating + total_perfect_rating) == 0:
                rate.employee_rate = 'No Rating'
            else:
                er = self.env['employee.rating'].search([('name_seq', '=', rate.name_seq)])
                average = ((total_bad_rating * 1) + (total_good_rating * 2) + (total_perfect_rating * 3)) / (
                        total_bad_rating + total_good_rating + total_perfect_rating)
                if average >= 2.5:
                    rate.employee_rate = 'Perfect'
                    er.employee_rate = 'Perfect'
                elif (average >= 2 and average < 2.5):
                    rate.employee_rate = 'Good'
                    er.employee_rate = 'Good'
                elif average < 2:
                    rate.employee_rate = 'Bad'
                    er.employee_rate = 'Bad'

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
        for rec in self:
            self.env['employee.rating'].create({
                'name_seq': rec.name_seq,
                'name': rec.name,
                'employee_rate': rec.employee_rate,
            })
        return result


class Family(models.Model):
    _name = 'hr.family'

    name = fields.Text("Full Name")
    day_of_birth = fields.Date("Date Of Birth")
    nationality = fields.Many2one('res.country', string='Nationality')
    ethnic_group = fields.Char("Ethnic Group")
    permanent_address = fields.Text("Permanent Address")
    family_id = fields.Many2one('hr.employee')
