from odoo import api, fields, models, _


class Assignment(models.Model):
    _name = "assignment.s"
    _inherit = ["mail.thread"]

    name = fields.Char(string='ID', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))
    department = fields.Many2one('hr.department', string="Department", required=True,
                                 default=lambda self: self.env.user.department_id)
    employee = fields.Many2one('hr.employee', string='Employee', required=True)
    deadline = fields.Datetime(string='Deadline', required=True, tracking=True)
    description = fields.Html(string='Description', tracking=True)
    state = fields.Selection(
        [('draft', 'Draft'),
         ('send', 'Sent'),
         ('complete', 'Completed'),
         ('confirm', 'Confirmed')
         ], string='Status', default='draft', readonly=True, tracking=True, group_expand='_read_group_selection_field'
    )
    creator = fields.Many2one('hr.employee', string="Creator", default=lambda self: self.env.user.employee_id)
    project_id = fields.Many2one('project.s', string='Project')
    project_right = fields.Boolean(string='In The Project')
    name_pm = fields.Many2one('hr.employee', related='project_id.name_pm', string='PM Name')
    create_date = fields.Date("Create Date", default=fields.Date.today)
    create_time = fields.Char("Create Time",
                              default=lambda self: fields.datetime.now().strftime('%H:%M'))
    start_date = fields.Date(string="Start Date", related='project_id.start_date')
    file = fields.Binary(string='Attached Files', tracking=True)
    file_name = fields.Char(string="File Name")
    reply_file = fields.Binary(string='Attached Files', tracking=True)
    reply_file_name = fields.Char(string='Reply File Name')
    reply_description = fields.Html(string='Reply', tracking=True)
    color = fields.Integer('Color Index', compute="set_kanban_color")
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Medium'),
        ('2', 'High')
    ], default='0', tracking=True)
    topic = fields.Many2one('topic.category', string="Topic", required=True, tracking=True)
    type = fields.Char(string='Type', default='1')
    create_subtask = fields.Boolean(string="Subtask?", tracking=True)
    subtask = fields.Many2one('assignment.s', string="Parent")
    subtask_count = fields.Integer(string='Subtask Qty', compute='_compute_subtask_count')
    rating = fields.Selection([
        ('no', 'Not Rating'),
        ('bad', 'Bad'),
        ('good', 'Good'),
        ('perfect', 'Perfect')
    ], default='no', tracking=True)

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '%s - %s' % (('[' + rec.name + ']'), rec.topic.name)))
        return res

    def _compute_subtask_count(self):
        for rec in self:
            subtask_count = self.env['assignment.s'].search_count([('subtask', '=', rec.id)])
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
                'message': 'The assignment has been confirmed',
                'type': 'rainbow_man',
                'img_url': 'He-Thong-Giao-Viec/static/img/confirmed.png'
            }
        }

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
            'create_subtask': self.create_subtask,
            'subtask': self.subtask.id,

        }
        self.env['my.assignment'].create(vals)

        # message = {
        #     'type': 'ir.actions.client',
        #     'tag': 'display_notification',
        #     'params': {
        #         'title': _('Hello!'),
        #         'message': 'You received assignment name: ' + self.name,
        #         'sticky': False,
        #     }
        # }
        # return message
        self.sudo().write({
            'state': 'send'
        })
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'The assignment has been sent',
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

    def write(self, vals):
        ch = super(Assignment, self).write(vals)
        for rec in self:
            self.env['my.assignment'].search([('name', '=', rec.name)]).write({
                'description': rec.description,
                'department': rec.department.id,
                'employee': rec.employee.id,
                'deadline': rec.deadline,
                'project_id': rec.project_id.id,
                'project_right': rec.project_right,
                'name_pm': rec.name_pm,
                'start_date': rec.start_date,
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

    @api.model
    def _read_group_selection_field(self, values, domain, order):
        return ['draft', 'send', 'complete', 'confirm']

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('assignment.s.sequence') or _('New')
        result = super(Assignment, self).create(vals)
        return result

    @api.onchange('topic')
    def assignment_only(self):
        for rec in self:
            return {'domain': {'topic': [('type', '=', rec.type), ('department', '=', rec.department.id)]}}

    @api.onchange('department')
    def related_department(self):
        for rec in self:
            return {'domain': {'employee': [('department_id', '=', rec.department.id)]}}
