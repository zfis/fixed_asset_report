# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, except_orm, UserError


class FixedAssetScheduleReport(models.Model):
    _name = "fixed.asset.register.report"

    category_id = fields.Many2one("account.asset.category", string = 'Asset Category')
    asset_id = fields.Many2one("account.asset.asset", string = 'Asset')
    asset_code = fields.Char(string = 'Asset Code')
    asset_name = fields.Char(string = 'Asset Name')
    manufacturer = fields.Char(string = 'Manufacturer')
    serial_number = fields.Char(string = 'Serial Number')
    model_number = fields.Char(string = 'Model Number')
    purchase_date = fields.Date(string = 'Purchase Date')
    cost = fields.Float(string = 'Cost', default = 0)
    accumulated_depreciation = fields.Float(string = 'Accumulated Depreciation', default = 0)
    net_book = fields.Float(string = 'Net Book', default = 0)
    
    month = fields.Char(string = 'Month')
    currency_id = fields.Many2one("res.currency", string = 'Currency')

