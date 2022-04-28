import datetime

from odoo import api, fields, models, _
from datetime import datetime


class Assistance(models.Model):
    _name = "assistance.s"
    _inherit = ["mail.thread"]

    name = fields.Char(string='ID', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))
    department = fields.Many2one('hr.department', string="Department", required=True)
    employee = fields.Many2one('hr.employee', string='Employee', required=True)
    deadline = fields.Datetime(string='Deadline', required=True)
    description = fields.Html(string='Description')
    state = fields.Selection(
        [('draft', 'Draft'),
         ('send', 'Sent'),
         ('complete', 'Completed'),
         ('confirm', 'Confirmed')
         ], string='Status', default='draft', readonly=True, tracking=True, group_expand='_read_group_selection_field'
    )
    creator = fields.Many2one('hr.employee', string="Creator", default=lambda self: self.env.user.employee_id)
    create_date = fields.Date("Create Date", default=fields.Date.today)
    create_time = fields.Char("Create Time",
                              default=lambda self: fields.datetime.now().strftime('%H:%M'))
    file = fields.Binary(string='Attached Files')
    file_name = fields.Char(string="File Name")
    reply_file = fields.Binary(string='Attached Files', tracking=True)
    reply_file_name = fields.Char(string='Reply File Name')
    reply_description = fields.Html(string='Reply')
    color = fields.Integer('Color Index', compute="set_kanban_color")
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Medium'),
        ('2', 'High')
    ], default='0')
    topic = fields.Many2one('topic.category', string="Topic", required=True)
    type = fields.Char(string='Type', default='2')
    create_subtask = fields.Boolean(string="Subtask?")
    subtask = fields.Many2one('assistance.s', string="Parent")
    subtask_count = fields.Integer(string='Subtask Qty', compute='_compute_subtask_count')
    rating = fields.Selection([
        ('no', 'Not Rating'),
        ('bad', 'Bad'),
        ('good', 'Good'),
        ('perfect', 'Perfect')
    ], default='no')

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '%s - %s' % (('[' + rec.name + ']'), rec.topic.name)))
        return res

    def _compute_subtask_count(self):
        for rec in self:
            subtask_count = self.env['assistance.s'].search_count([('subtask', '=', rec.id)])
            rec.subtask_count = subtask_count

    def action_confirm(self):
        vals = {
            'state': 'confirm',
        }
        for rec in self:
            self.env['my.assignment'].search([('name', '=', rec.name)]).write(vals)
        self.sudo().write({
            'state': 'confirm'
        })
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'The assistance has been confirmed',
                'type': 'rainbow_man',
                'img_url': 'He-Thong-Giao-Viec/static/img/confirmed.png'
            }
        }

    def send_assistance(self):
        vals = {
            'name': self.name,
            'description': self.description,
            'department': self.department.id,
            'employee': self.employee.id,
            'deadline': self.deadline,
            'file': self.file,
            'file_name': self.file_name,
            'create_time': self.create_time,
            'priority': self.priority,
            'topic': self.topic.id,
            'creator': self.creator.id,
            'type': self.type,
        }
        self.env['my.assignment'].create(vals)
        self.sudo().write({
            'state': 'send'
        })
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'The assistance has been sent',
                'type': 'rainbow_man',
                'img_url': 'He-Thong-Giao-Viec/static/img/sent.png'
            }
        }

    def set_kanban_color(self):
        for record in self:
            if record.priority == '0':
                color = 0
            elif record.priority == '1':
                color = 2
            elif record.priority == '2':
                color = 1
            else:
                color = 1
            record.color = color

    @api.model
    def _read_group_selection_field(self, values, domain, order):
        return ['draft', 'send', 'complete', 'confirm']

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('assistance.s.sequence') or _('New')
        result = super(Assistance, self).create(vals)
        return result

    def write(self, vals):
        ch = super(Assistance, self).write(vals)
        for rec in self:
            self.env['my.assignment'].search([('name', '=', rec.name)]).write({
                'description': rec.description,
                'department': rec.department.id,
                'employee': rec.employee.id,
                'deadline': rec.deadline,
                'file': rec.file,
                'file_name': rec.file_name,
                'create_time': rec.create_time,
                'priority': rec.priority,
                'topic': rec.topic.id,
                'creator': rec.creator.id,
                'create_subtask': rec.create_subtask,
                'subtask': rec.subtask.id,
                'rating': rec.rating,

            })
        return ch

    @api.onchange('department')
    def assistance_only(self):
        for rec in self:
            return {'domain': {'topic': [('type', '=', rec.type), ('department', '=', rec.department.id)]}}

    @api.onchange('department')
    def related_department(self):
        for rec in self:
            # print('print:....', rec.current_user)
            return {'domain': {'employee': [('department_id', '=', rec.department.id)]}}
