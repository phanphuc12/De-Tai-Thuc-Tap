from odoo import api, fields, models, _


class assignment(models.Model):
    _name = "assignment.s"
    _inherit = ["mail.thread"]

    name = fields.Char(string='ID', required=True, copy=False, readonly=True, index=True,
                           default=lambda self: _('New'))
    department = fields.Many2one('hr.department', string="Department", required=True)
    employee = fields.Many2one('res.users', string='Employee', required=True)
    deadline = fields.Datetime(string='Deadline', required=True)
    description = fields.Text(string='Description')
    # name_seq = fields.Char(string='ID', required=True, copy=False, readonly=True, index=True,
    #                        default=lambda self: _('New'))
    state = fields.Selection(
        [('draft', 'Draft'),
         ('send', 'Sent'),
         ('complete', 'Completed'),
         ('confirm', 'Confirmed')
         ], string='Status', default='draft', readonly=True, tracking=True
    )
    current_user = fields.Many2one('res.users', 'Current User', default=lambda self: self.env.user, readony=True)

    def send_assignment(self):
        vals = {
            'name': self.name,
            'description': self.description,
            'department': self.department.id,
            'employee': self.employee.id,
            # 'name_seq': self.name_seq,
            'deadline': self.deadline,

        }
        for rec in self:
            rec.state = 'send'
            # print('print:....', rec.current_user)
        self.env['my.assignment'].create(vals)

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'
            ma = self.env['my.assignment'].search([('name', '=', rec.name)])
            if ma.name:
                ma.state = "confirm"

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('assignment.s.sequence') or _('New')
        result = super(assignment, self).create(vals)
        return result

    @api.onchange('department')
    def related_department(self):
        for rec in self:
            # print('print:....', rec.current_user)
            return {'domain': {'employee': [('department_id', '=', rec.department.id)]}}
