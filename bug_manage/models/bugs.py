

# -*- coding: utf-8 -*-
from odoo import models, fields, api

class bug(models.Model):
    _name = 'bm.bug'
    _description = 'bug bug bug'

    name = fields.Char('Bug 簡述',required=True)
    detail = fields.Text(size=150)
    is_closed = fields.Boolean('是否要關閉')
    close_reason = fields.Selection(
        [('changed','已修改AAA'),('cannot','無法修改'),('delay','推遲')]
        ,string="關閉的理由"
    )
    user_id = fields.Many2one('res.users',string='負責人')
    follower_id = fields.Many2many('res.partner',string='關注者')

    def test_only(self, param1, param2):
        print(param1)
        print(param2)
        print(param1 * param2)
        return True

    def do_close(self):

        print(self.env.user)
        print(self.env.cr)
        print(self.env.su)
        print(self.env.context)

        partner_id = self.env['res.partner'].search([])
        print(partner_id)
        parner_name = partner_id.mapped('name')
        print(parner_name)
        partner_browse = self.env['res.partner'].browse([11, 20, 22, 31, 23])
        print(partner_browse)
        parner_browse_name = partner_browse.mapped('name')
        print(parner_browse_name)


       # print(self.env['res.partner'].search([['is_company', '=', True]]))
        for item in self:
            if item.is_closed:
                item.is_closed=False
                return False
            else:
                item.is_closed=True
                return True




