from odoo import fields, models, api, _


class SendAssignment(models.TransientModel):
    _name = "send.assignment"

    description = fields.Text(string='Description', required=False)
    department = fields.Many2one('hr.department', string="Department")
    employee = fields.Many2one('hr.employee', string='Employee')
    deadline = fields.Datetime(string='Deadline')
    name_seq = fields.Char(string='ID', copy=False, readonly=True, index=True)



    def send_assignment(self):
        vals = {
            'description': self.description,
            'department': self.department,
            'employee': self.employee,
            'name_seq': self.name_seq,
            'deadline': self.deadline,


        }
        self.env['my.assignment'].create(vals)
