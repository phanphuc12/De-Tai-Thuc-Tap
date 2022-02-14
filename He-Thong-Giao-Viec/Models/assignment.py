from odoo import api, fields, models, _


class assignment(models.Model):
    _name = "assignment.s"
    _inherit = ["mail.thread"]

    department = fields.Many2one('hr.department', string="Department", required=True)
    employee = fields.Many2one('hr.employee', string='Employee', required=True)
    deadline = fields.Datetime(string='Deadline', required=True)
    description = fields.Text(string='Description')
    name_seq = fields.Char(string='ID', required=True, copy=False, readonly=True, index=True,
                           default=lambda self: _('New'))
    status = fields.Selection(
        [('draft', 'Draft'),
         ('send', 'Send'),
         ('completed', 'Completed'),
         ('confirmed', 'Confirmed')
         ], string='Status', default='draft', readonly=True
    )

    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('assignment.s.sequence') or _('New')
        result = super(assignment, self).create(vals)
        return result

    @api.onchange('department')
    def related_department(self):
        for rec in self:
            return {'domain': {'employee': [('department_id', '=', rec.department.id)]}}

    def send_assignment(self):
        vals = {
            'description': self.description,
            'department': self.department.id,
            'employee': self.employee.id,
            'name_seq': self.name_seq,
            'deadline': self.deadline,

        }
        self.env['my.assignment'].create(vals)
