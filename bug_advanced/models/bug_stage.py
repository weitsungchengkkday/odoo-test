# -*- coding: utf-8 -*-

from odoo import models, fields, api

class BugStage(models.Model):
    _name = 'bm.bug.stage'
    _description = '除蟲階段'
    _order = 'sequence,name'

    name = fields.Char('階段名稱')
    sequence = fields.Integer('階段序列')

    desc_detail = fields.Text('蟲的詳述')
    status = fields.Selection([
        ('waiting','未開始'),
        ('doing','進行中'),
        ('closed','關閉'),
        ('rework','重新測試'),
    ],
    '狀態',
    )

    document = fields.Html('文檔')
    percent_pro = fields.Float('進度', (3,2))
    deadline = fields.Date('治好蟲的最後期限')
    create_on = fields.Datetime('創建日期', default=lambda self:fields.Datetime.now())
    delay = fields.Boolean('是否延誤')
    image = fields.Binary('圖片')

    bug_ids = fields.One2many(
        'bm.bug',
        'stage_id',
        '蟲兒1',
    )