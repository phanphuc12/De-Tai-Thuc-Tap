from odoo import api, fields, models, tools, _


class Board(models.AbstractModel):
    _name = 'board.board'
    _inherit = 'board.board'

    st = fields.Text('Test')
