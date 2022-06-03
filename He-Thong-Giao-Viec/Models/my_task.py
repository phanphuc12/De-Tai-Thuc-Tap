from odoo import api, fields, models


class MyTask(models.Model):
    _name = "task.management"

    name = fields.Char('Name', required=True)
    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date', required=True)
    description = fields.Html('Description')
    assignment = fields.Many2one('assignment.s', string='Related Work')
    creator = fields.Many2one('hr.employee', default=lambda self: self.env.user.employee_id)
    project_id = fields.Many2one('project.s', string='Project', related='assignment.project_id')
    project_right = fields.Boolean(string='In The Project', related='assignment.project_right')
    name_pm = fields.Many2one('hr.employee', string='PM Name', related='assignment.name_pm')
    file = fields.Binary(string='Attached Files', related='assignment.file')
    file_name = fields.Char(string="File Name", related='assignment.file_name')
    topic = fields.Many2one('topic.category', string="Topic", related='assignment.topic')
    deadline = fields.Datetime(string='Deadline', related='assignment.deadline')
    state_id = fields.Selection([
        ('todo', 'To Do'),
        ('doing', 'Doing'),
        ('done', 'Done')
    ], default='todo', group_expand='_read_group_selection_field')
    sprint = fields.Many2one('sprint.management', string='Sprint', required=True)
    color = fields.Integer('Color Index', compute="set_kanban_color")
    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], default='low', string='Priority', group_expand='_read_group_selection_priority')

    def set_priority_low(self):
        for rec in self:
            rec.priority = 'low'

    def set_priority_medium(self):
        for rec in self:
            rec.priority = 'medium'

    def set_priority_high(self):
        for rec in self:
            rec.priority = 'high'

    def set_kanban_color(self):
        for record in self:
            if record.priority == 'low':
                color = 0
            elif record.priority == 'medium':
                color = 2
            elif record.priority == 'high':
                color = 1
            else:
                color = 1
            record.color = color

    # @api.onchange('name')
    # def related_department(self):
    #     for rec in self:
    #         return {'domain': {'sprint': [('creator', '=', rec.creator)]}}

    @api.model
    def _read_group_selection_field(self, values, domain, order):
        return ['todo', 'doing', 'done']

    @api.model
    def _read_group_selection_priority(self, values, domain, order):
        return ['low', 'medium', 'high']
