from odoo import fields, models, api, _


class DenyWizard(models.TransientModel):
    _name = "deny.wizard"

    reason_deny = fields.Text(string='reason')
    name = fields.Char('nothing')

    def action_deny_assignment(self):
        ma = self.env['assignment.s'].browse(self.env.context.get('active_id'))
        send_reason = self.env['my.assignment'].search([('name', '=', ma.name)]).write({
            'reason_deny': self.reason_deny,
            'state': 'received',
        })
        change_status = self.env['assignment.s'].browse(self.env.context.get('active_id')).write({
            'state': 'send',
        })
        return send_reason, change_status

    def action_deny_assistance(self):
        ma = self.env['assistance.s'].browse(self.env.context.get('active_id'))
        send_reason = self.env['my.assignment'].search([('name', '=', ma.name)]).write({
            'reason_deny': self.reason_deny,
            'state': 'received',
        })
        change_status = self.env['assistance.s'].browse(self.env.context.get('active_id')).write({
            'state': 'send',
        })

        return send_reason, change_status
