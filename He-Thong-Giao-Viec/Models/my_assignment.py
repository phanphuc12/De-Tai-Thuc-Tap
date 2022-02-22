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
    state = fields.Selection(
        [('received', 'Received'),
         ('complete', 'Completed'),
         ('confirm', 'Confirmed')
         ], string='Status', default='received', readonly=True, tracking=True)
    current_user = fields.Many2one('res.users', 'Creator', default=lambda self: self.env.user, readonly=True)
    project_id = fields.Many2one('project.s', string='Project')
    project_right = fields.Boolean(string='In The Project')
    name_pm = fields.Many2one('res.users', related='project_id.name_pm', string='PM Name')
    start_date = fields.Date(string="Start Date", related='project_id.start_date')
    file = fields.Binary(string='Attached Files')
    file_name = fields.Char(string="File Name")
    reply_file = fields.Binary(string='Attached Files', tracking=True)
    reply_file_name = fields.Char(string='Reply File Name')

    def action_complete(self):
        for rec in self:
            rec.state = 'complete'
            ma = self.env['assignment.s'].search([('name', '=', rec.name)])
            if ma.name:
                ma.state = "complete"
                ma.reply_file = rec.reply_file
                ma.reply_file_name = rec.reply_file_name
                print('check...', ma.state)

