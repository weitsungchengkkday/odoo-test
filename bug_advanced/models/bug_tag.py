# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BugTag(models.Model):
    _name = 'bm.bug.tag'
    _description = '除蟲任務標籤'
    name = fields.Char('標籤名稱')
    bug_ids=fields.Many2many(
        comodel_name='bm.bug',
        relation='bug_tag_rel',
        column1='tag_id',
        column2='bug_id',
        string='蟲兒2',
    )
