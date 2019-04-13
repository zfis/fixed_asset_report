# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, except_orm, UserError


class FixedAssetScheduleReport(models.Model):
    _name = "fixed.asset.schedule.report"

    category_id = fields.Many2one("account.asset.category", string = 'Asset Category')
    currency_id = fields.Many2one("res.currency", string = 'Currency')
    search_start_date = fields.Date(string = 'Search Start Date')
    search_end_date = fields.Date(string = 'Search End Date')

    opening_balance_cost = fields.Float(string = 'Opening Balance', default = 0)
    addition_cost = fields.Float(string = 'Addition During Period', default = 0)
    disposal_cost = fields.Float(string = 'Disposal During Period', default = 0)
    closing_balance_cost = fields.Float(string = 'Closing Balance', default = 0)

    opening_balance_accumulated_depreciation = fields.Float(string = 'Opening Balance', default = 0)
    depreciation_accumulated_depreciation = fields.Float(string = 'Depreciation Charge During Period', default = 0)
    disposal_accumulated_depreciation = fields.Float(string = 'Disposal During Period', default = 0)
    closing_balance_accumulated_depreciation = fields.Float(string = 'Closing Balance', default = 0)

    net_book = fields.Float(string = 'Net Book', default = 0)

