from odoo import fields, models, api, _


class MyAssignment(models.Model):
    _name = "my.assignment"
    _inherit = ["mail.thread"]
    _description = "My Assignment"

    name = fields.Char(string='ID', required=True, copy=False, readonly=True, index=True,
                           default=lambda self: _('New'))
    department = fields.Many2one('hr.department', string="Department", required=True)
    employee = fields.Many2one('hr.employee', string='Employee', required=True)
    deadline = fields.Datetime(string='Deadline', required=True)
    description = fields.Text(string='Description')
    # name_seq = fields.Char(string='ID', required=True, copy=False, readonly=True, index=True,
    #                        default=lambda self: _('New'))
    state = fields.Selection(
        [('received', 'Received'),
         ('complete', 'Completed'),
         ('confirm', 'Confirmed')
         ], string='Status', default='received', readonly=True, tracking=True)
    current_user = fields.Many2one('res.users', 'Current User', default=lambda self: self.env.user, readonly=True)

    def action_complete(self):
        for rec in self:
            rec.state = 'complete'
            ma = self.env['assignment.s'].search([('name', '=', rec.name)])
            if ma.name:
                ma.state = "complete"
                print('check...', ma.state)
