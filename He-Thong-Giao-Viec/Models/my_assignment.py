from odoo import fields, models, api, _


class MyAssignment(models.Model):
    _name = "my.assignment"
    _inherit = ["mail.thread"]
    _description = "My Assignment"

    name = fields.Char(string='ID', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))
    department = fields.Many2one('hr.department', string="Department", required=True)
    employee = fields.Many2one('hr.employee', string='Employee', required=True)
    deadline = fields.Datetime(string='Deadline', required=True, tracking=True)
    create_date = fields.Date("Create Date", default=fields.Date.today)
    create_time = fields.Char("Create Time",
                              default=lambda self: fields.datetime.now().strftime('%H:%M'))
    description = fields.Html(string='Description', tracking=True)
    state = fields.Selection(
        [('received', 'Received'),
         ('complete', 'Completed'),
         ('confirm', 'Confirmed')
         ], string='Status', default='received', readonly=True, tracking=True,
        group_expand='_read_group_selection_field')
    creator = fields.Many2one('hr.employee', string="Creator", readonly=True)
    project_id = fields.Many2one('project.s', string='Project')
    project_right = fields.Boolean(string='In The Project')
    name_pm = fields.Many2one('hr.employee', related='project_id.name_pm', string='PM Name')
    start_date = fields.Date(string="Start Date", related='project_id.start_date')
    file = fields.Binary(string='Attached Files', tracking=True)
    file_name = fields.Char(string="File Name")
    reply_file = fields.Binary(string='Attached Files', tracking=True)
    reply_file_name = fields.Char(string='Reply File Name')
    reply_description = fields.Html(string="Reply", tracking=True)
    color = fields.Integer('Color Index', compute="set_kanban_color")
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Medium'),
        ('2', 'High')
    ], default='0', tracking=True)
    topic = fields.Many2one('topic.category', string="Topic", tracking=True)
    type = fields.Selection([
        ('1', 'Assignment'),
        ('2', 'Assistance')
    ], string='type')
    create_subtask = fields.Boolean(string="Subtask?", tracking=True)
    subtask = fields.Many2one('assignment.s', string="Parent")
    subtask_count = fields.Integer(compute='_compute_subtask_count')
    reason_deny = fields.Text(string='Reason')
    rating = fields.Selection([
        ('no', 'Not Rating'),
        ('bad', 'Bad'),
        ('good', 'Good'),
        ('perfect', 'Perfect')
    ], default='no', tracking=True)
    count_completed_job = fields.Integer('count completed job')
    employee_rate = fields.Char('Employee Rate Final', compute='rating_employee')
    current_uid = fields.Many2one('res.users', string='Current User', compute='get_current_user')
    current_record = fields.Many2one('my.assignment', string='Current Records', compute='get_current_record')

    def get_current_record(self):
        for rec in self:
            current_rec = self.enc['my.assignment'].search([('employee.user_id', '=', self.env.context.get('uid'))])
            rec.current_record = current_rec
            print(rec.current_record)

    def get_current_user(self):
        for user in self:
            get_user = self.env['res.users'].browse([('user_id', '=', self.env.context.get('uid'))])
            user.current_uid = get_user
            print(user.current_uid)

    def compute_completed_job(self):
        for rec in self:
            cj = self.env['my.assignment'].search_count([('state', '=', 'confirmed')])
            rec.count_completed_job = cj

    def _compute_subtask_count(self):
        for rec in self:
            subtask_count = self.env['assignment.s'].search_count([('subtask', '=', rec.id)])
            rec.subtask_count = subtask_count

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

    def action_complete(self):
        for rec in self:
            if rec.type == '1':
                self.env['assignment.s'].search([('name', '=', self.name)]).write({
                    'state': 'complete',
                    'reply_file': self.reply_file,
                    'reply_file_name': self.reply_file_name,
                    'reply_description': self.reply_description,
                })
            else:
                self.env['assistance.s'].search([('name', '=', self.name)]).write({
                    'state': 'complete',
                    'reply_file': self.reply_file,
                    'reply_file_name': self.reply_file_name,
                })
        self.sudo().write({
            'state': 'complete'
        })
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'The result has been sent',
                'type': 'rainbow_man',
                'img_url': 'He-Thong-Giao-Viec/static/img/complete.png'
            }
        }

    @api.model
    def _read_group_selection_field(self, values, domain, order):
        return ['received', 'complete', 'confirm']
