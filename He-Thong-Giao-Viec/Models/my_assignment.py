from odoo import fields, models, api, _


class MyAssignment(models.Model):
    _name = "my.assignment"
    _description = "My Assignment"

    department = fields.Many2one('hr.department', string="Department", required=True)
    employee = fields.Many2one('hr.employee', string='Employee', required=True)
    deadline = fields.Datetime(string='Deadline', required=True)
    description = fields.Text(string='Description')
    name_seq = fields.Char(string='ID', required=True, copy=False, readonly=True, index=True,
                           default=lambda self: _('New'))
    state = fields.Selection(
        [('received', 'Received'),
         ('complete', 'Completed'),
         ('confirm', 'Confirmed')
         ], string='Status', default='received', readonly=True)

    def action_complete(self):
        for rec in self:
            rec.state = 'complete'
            ma = self.env['assignment.s'].search([('name_seq', '=', rec.name_seq)])
            if ma.name_seq:
                ma.state = "complete"
                # print('check...', ma.state)

    # @api.onchange('state')
    # def state_complete(self):
    #     for rec in self:
    #         ma = self.env['assignment.s'].search([('name_seq', '=', rec.name_seq)])
    #         if ma:
    #             print("test...", ma.name_seq)
