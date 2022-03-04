import datetime

from odoo import api, fields, models, _
from datetime import datetime


class assignment(models.Model):
    _name = "assignment.s"
    _inherit = ["mail.thread"]

    name = fields.Char(string='ID', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))
    department = fields.Many2one('hr.department', string="Department", required=True)
    employee = fields.Many2one('res.users', string='Employee', required=True)
    deadline = fields.Datetime(string='Deadline', required=True)
    description = fields.Text(string='Description')
    state = fields.Selection(
        [('draft', 'Draft'),
         ('send', 'Sent'),
         ('complete', 'Completed'),
         ('confirm', 'Confirmed')
         ], string='Status', default='draft', readonly=True, tracking=True
    )
    creator = fields.Many2one('res.users', string='Creator', default=lambda self: self.env.user)
    project_id = fields.Many2one('project.s', string='Project')
    project_right = fields.Boolean(string='In The Project')
    name_pm = fields.Many2one('hr.employee', related='project_id.name_pm', string='PM Name')
    create_date = fields.Date("Create Date", default=fields.Date.today)
    create_time = fields.Char("Create Time",
                              default=lambda self: fields.datetime.now().strftime('%H:%M'))
    start_date = fields.Date(string="Start Date", related='project_id.start_date')
    file = fields.Binary(string='Attached Files')
    file_name = fields.Char(string="File Name")
    reply_file = fields.Binary(string='Attached Files', tracking=True)
    reply_file_name = fields.Char(string='Reply File Name')
    color = fields.Integer('Color Index', compute="set_kanban_color")
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Medium'),
        ('2', 'High')
    ], default='0')
    topic = fields.Many2one('topic.category', string="Topic", required=True)
    type = fields.Char(string='Type', default='1')

    # id_search = fields.Many2one('assignment.s', string='check_id', default="check_id")
    #
    # def check_id(self):
    #     for rec in self:
    #         rec.id_search = rec.name
    #         print(rec.id_search)

    def action_confirm(self):
        # print(self)
        vals = {
            'state': 'confirm',
        }
        for rec in self:
            rec.state = 'confirm'
            # print('check...', vals)
            self.env['my.assignment'].search([('name', '=', rec.name)]).write(vals)

    def action_decline(self):
        for rec in self:
            rec.state = 'send'
            self.env['my.assignment'].search([('name', '=', rec.name)]).write({
                'state': 'received'
            })

    def send_assignment(self):
        vals = {
            'name': self.name,
            'description': self.description,
            'department': self.department.id,
            'employee': self.employee.id,
            'deadline': self.deadline,
            'project_id': self.project_id.id,
            'project_right': self.project_right,
            'name_pm': self.name_pm,
            'start_date': self.start_date,
            'file': self.file,
            'file_name': self.file_name,
            'create_time': self.create_time,
            'priority': self.priority,
            'topic': self.topic.id,
            'creator': self.creator.id,
            'type': self.type,

        }
        for rec in self:
            rec.state = 'send'
        self.env['my.assignment'].create(vals)

    def set_kanban_color(self):
        for record in self:
            if record.state == 'draft':
                color = 0
            elif record.state == 'send':
                color = 3
            elif record.state == 'complete':
                color = 4
            elif record.state == 'confirm':
                color = 10
            else:
                color = 1
            record.color = color

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('assignment.s.sequence') or _('New')
        result = super(assignment, self).create(vals)
        return result

    def write(self, vals):
        for rec in self:
            pr = self.env['my.assignment'].search([('name', '=', rec.name)]).write(vals)
            ch = super(assignment, self).write(vals)
            return pr, ch

    @api.onchange('topic')
    def assignment_only(self):
        for rec in self:
            return {'domain': {'topic': [('type', '=', rec.type)]}}

    @api.onchange('department')
    def related_department(self):
        for rec in self:
            return {'domain': {'employee': [('department_id', '=', rec.department.id)]}}


class AssignmentSearchPanel(models.Model):
    _name = "assignment.search.panel"

    check_id = fields.Many2one('assignment.s', string='ID')
