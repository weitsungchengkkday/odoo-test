# -*- coding: utf-8 -*-

from odoo import models, fields, api

class BugAdvance(models.Model):
    _inherit = 'bm.bug'

    name = fields.Char(help='簡述這隻蟲的樣子')
    need_time = fields.Integer('治好這隻蟲需要的時間')
    stage_id = fields.Many2one('bm.bug.stage', '階段')

    tag_ids = fields.Many2many(
        comodel_name='bm.bug.tag',
        relation='bug_tag_rel',
        column1='bug_id',
        column2='tag_id',
        string='標示',
    )

    @api.onchange('user_id')
    def user_follower_ref(self):
        if not self.user_id:
            self.follower_id = None
            return {
                'warning': {
                    'title': '缺少負責人',
                    'message': '清空關注者'
                },
                # 'domain': {'follower_id': [('x_is_teacher', '=', True)]}
            }





