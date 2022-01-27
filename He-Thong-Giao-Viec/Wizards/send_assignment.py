from odoo import fields, models, api, _


class SendAssignment(models.TransientModel):
    _name = "send.assignment"

    description = fields.Text(string='Description', required=False)


    def send_assignment(self):
        vals = {
            'description': self.description
        }
        self.env['my.assignment'].create(vals)
