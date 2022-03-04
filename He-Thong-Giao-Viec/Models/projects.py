from odoo import api, fields, models, _


class Projects(models.Model):
    _name = "project.s"
    _inherit = ["mail.thread"]

    name = fields.Char(string='ID', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))
    project = fields.Char(string="Project Name", required=True)
    department = fields.Many2many('hr.department', string='Department', required=True)
    name_pm = fields.Many2one('hr.employee', string='PM Name', required=True)
    start_date = fields.Date(string="Start Date", requied=True)
    description = fields.Text(string="Description")

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('project.s.sequence') or _('New')
        result = super(Projects, self).create(vals)
        return result

    @api.onchange('department')
    def related_department(self):
        for rec in self:
            return {'domain': {'name_pm': [('department_id', '=', rec.department.ids)]}}
