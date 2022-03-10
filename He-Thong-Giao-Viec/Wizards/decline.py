from odoo import fields, models, api, _


class DeclineWizard(models.TransientModel):
    _name = "decline.wizard"

    reason_decline = fields.Text(string='reason')
    name = fields.Char('nothing')

    def action_decline(self):
        ma = self.env['assignment.s'].browse(self.env.context.get('active_id'))
        send_reason = self.env['my.assignment'].search([('name', '=', ma.name)]).write({
            'reason_decline': self.reason_decline,
            'state': 'received',
        })
        change_status = self.env['assignment.s'].browse(self.env.context.get('active_id')).write({
            'state': 'send',
        })
        return send_reason, change_status
