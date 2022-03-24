from odoo import api, fields, models, _


class Sprint(models.Model):
    _name = "sprint.management"

    name = fields.Char('Name', required=True)
    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date', required=True)
    description = fields.Text('description', required=False)

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '%s - %s' % (rec.name, ('(' + str(rec.start_date.strftime('%d/%m/%Y')) + ' - ' + str(
                rec.end_date.strftime('%d/%m/%Y')) + ')'))))
        return res
