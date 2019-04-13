# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, except_orm, UserError
import calendar


class AccountAssetAsset(models.Model):
    _inherit = "account.asset.asset"

    asset_code = fields.Char(string = 'Asset Code', readonly=True)
    manufacturer = fields.Char(string = 'Manufacturer')
    serial_number = fields.Char(string = 'Serial Number')
    model_number = fields.Char(string = 'Model Number')

    @api.model
    def create(self, vals):
        vals['asset_code'] = self.env['ir.sequence'].next_by_code('account.asset.asset')
        res = super(AccountAssetAsset, self).create(vals)
        return res


class FixedAssetReportWizard(models.Model):
    _name = "fixed.asset.report.wizard"

    # from_date = fields.Date(string = 'From Date', required = True, default = fields.Date.today())
    # to_date = fields.Date(string = 'To Date', required = True, default = fields.Date.today())
    from_date = fields.Date(string = 'From Date')
    to_date = fields.Date(string = 'To Date')
    month = fields.Selection(
        string = 'Month',
        selection = [
            ('1', 'January'),
            ('2', 'February'),
            ('3', 'March'),
            ('4', 'April'),
            ('5', 'May'),
            ('6', 'June'),
            ('7', 'July'),
            ('8', 'August'),
            ('9', 'Setember'),
            ('10', 'October'),
            ('11', 'November'),
            ('12', 'December')
        ],
        default = ''
    )
    radio_selection = fields.Selection(
        string = 'Chose Report Type',
        selection = [
            ('0', 'Schedule'),
            ('1', 'Register')
        ],
        default = ''
    )
    
    
    @api.multi
    def action_fixed_asset_report_search_button(self):
        self.ensure_one()        
        name = _('Fixed Asset Report Search')

        company_id = self.env.user.company_id.id
        currency_id = self.env.user.company_id.currency_id.id
        month_search = self.month
        from_date_search = self.from_date
        to_date_search = self.to_date
        radio_selection_search = self.radio_selection
        search_start_date = datetime.now()
        search_end_date = datetime.now()


        ## Set Report Type
        if radio_selection_search == '1':
            from_date_search = ""
            to_date_search = ""
        
        
        ## Print Report
        if not from_date_search or not to_date_search:
            if not month_search:
                raise UserError("Select Month.")
            
            # search_month = month_search.capitalize()
            search_month = month_search

            ## Get Fixed Asset Schedule Report
            return self.print_fixed_asset_register_report(search_month, company_id, currency_id)
        else:
            search_start_date = datetime.strptime(from_date_search, '%Y-%m-%d').strftime('%m/%d/%Y')
            search_end_date = datetime.strptime(to_date_search, '%Y-%m-%d').strftime('%m/%d/%Y')

            ## Get Fixed Asset Schedule Report
            return self.print_fixed_asset_schedule_report(search_start_date, search_end_date, company_id, currency_id)
      

    @api.multi
    def print_fixed_asset_schedule_report(self, search_start_date, search_end_date, company_id, currency_id):
        ## Get Fixed Asset Schedule
        #condition_for_daterange = "AND (aaa.date BETWEEN '" + search_start_date + "' AND '" + search_end_date + "')"
        condition_for_daterange = ""
        condition_for_daterange_cost = "AND (date BETWEEN '" + search_start_date + "' AND '" + search_end_date + "')"
        condition_for_daterange_cost_OB = "AND (date < '" + search_start_date + "')"
        condition_for_daterange_accumulated_depreciation = "AND (line.depreciation_date BETWEEN '" + search_start_date + "' AND '" + search_end_date + "')"
        condition_for_daterange_accumulated_depreciation_OB = "AND (line.depreciation_date < '" + search_start_date + "')"
        self.env.cr.execute(""" SELECT
                                    aaa.category_id
                                    , ( CASE
                                            WHEN (SELECT sum(value) FROM account_asset_asset WHERE state = 'open' {0} AND category_id = aaa.category_id) IS NULL THEN '0'
                                            ELSE (SELECT sum(value) FROM account_asset_asset WHERE state = 'open' {1} AND category_id = aaa.category_id)
                                        END ) AS opening_balance_cost
                                    , ( CASE
                                            WHEN (SELECT sum(value) FROM account_asset_asset WHERE (state = 'open' OR state = 'close') {2} AND category_id = aaa.category_id) IS NULL THEN '0'
                                            ELSE (SELECT sum(value) FROM account_asset_asset WHERE (state = 'open' OR state = 'close') {3} AND category_id = aaa.category_id)
                                        END ) AS addition_cost
                                    , ( CASE
                                            WHEN (SELECT sum(value) FROM account_asset_asset WHERE state = 'close' {4} AND category_id = aaa.category_id) IS NULL THEN '0'
                                            ELSE (SELECT sum(value) FROM account_asset_asset WHERE state = 'close' {5} AND category_id = aaa.category_id)
                                        END ) AS disposal_cost
                                    , ( CASE
                                            WHEN (SELECT sum(line.amount) FROM account_asset_depreciation_line line LEFT JOIN account_asset_asset asset ON line.asset_id = asset.id WHERE asset.state = 'open' AND line.move_posted_check = true {6} AND asset.category_id = aaa.category_id) IS NULL THEN '0'
                                            ELSE (SELECT sum(line.amount) FROM account_asset_depreciation_line line LEFT JOIN account_asset_asset asset ON line.asset_id = asset.id WHERE asset.state = 'open' AND line.move_posted_check = true {7} AND asset.category_id = aaa.category_id)
                                        END ) AS opening_balance_accumulated_depreciation
                                    , ( CASE
                                            WHEN (SELECT sum(line.amount) FROM account_asset_depreciation_line line LEFT JOIN account_asset_asset asset ON line.asset_id = asset.id WHERE asset.state = 'open' AND line.move_posted_check = true {8} AND asset.category_id = aaa.category_id) IS NULL THEN '0'
                                            ELSE (SELECT sum(line.amount) FROM account_asset_depreciation_line line LEFT JOIN account_asset_asset asset ON line.asset_id = asset.id WHERE asset.state = 'open' AND line.move_posted_check = true {9} AND asset.category_id = aaa.category_id)
                                        END ) AS depreciation_accumulated_depreciation
                                    , ( CASE
                                            WHEN (SELECT sum(line.amount) FROM account_asset_depreciation_line line LEFT JOIN account_asset_asset asset ON line.asset_id = asset.id WHERE asset.state = 'close' AND line.move_posted_check = true {10} AND asset.category_id = aaa.category_id) IS NULL THEN '0'
                                            ELSE (SELECT sum(line.amount) FROM account_asset_depreciation_line line LEFT JOIN account_asset_asset asset ON line.asset_id = asset.id WHERE asset.state = 'close' AND line.move_posted_check = true {11} AND asset.category_id = aaa.category_id)
                                        END ) AS disposal_accumulated_depreciation
                                FROM account_asset_asset aaa
                                WHERE aaa.company_id = %s
                                {12}
                                GROUP BY aaa.category_id; """.format(
                                                                        condition_for_daterange_cost_OB,
                                                                        condition_for_daterange_cost_OB,

                                                                        condition_for_daterange_cost,
                                                                        condition_for_daterange_cost,
                                                                        condition_for_daterange_cost,
                                                                        condition_for_daterange_cost,

                                                                        condition_for_daterange_accumulated_depreciation_OB,
                                                                        condition_for_daterange_accumulated_depreciation_OB,

                                                                        condition_for_daterange_accumulated_depreciation,
                                                                        condition_for_daterange_accumulated_depreciation,
                                                                        condition_for_daterange_accumulated_depreciation,
                                                                        condition_for_daterange_accumulated_depreciation,

                                                                        condition_for_daterange
                                                                    ), 
                                    ( 
                                        tuple(str(company_id)),
                                    ))
        res = self.env.cr.dictfetchall()


        ## Clear existing table data
        self.env.cr.execute(""" TRUNCATE TABLE fixed_asset_schedule_report ; """)

        
        ## Push new data to the table
        for item in res:
            item_closing_balance_cost = (float(item['opening_balance_cost']) + float(item['addition_cost'])) - float(item['disposal_cost'])
            item_closing_balance_accumulated_depreciation = (float(item['opening_balance_accumulated_depreciation']) + float(item['depreciation_accumulated_depreciation'])) - float(item['disposal_accumulated_depreciation'])
            item_net_book = item_closing_balance_cost - item_closing_balance_accumulated_depreciation

            self.env['fixed.asset.schedule.report'].create({
                'category_id': item['category_id'],
                'currency_id': currency_id,
                'search_start_date': search_start_date,
                'search_end_date': search_end_date,

                'opening_balance_cost': item['opening_balance_cost'],
                'addition_cost': item['addition_cost'],
                'disposal_cost': item['disposal_cost'],
                'closing_balance_cost': item_closing_balance_cost,

                'opening_balance_accumulated_depreciation': item['opening_balance_accumulated_depreciation'],
                'depreciation_accumulated_depreciation': item['depreciation_accumulated_depreciation'],
                'disposal_accumulated_depreciation': item['disposal_accumulated_depreciation'],
                'closing_balance_accumulated_depreciation': item_closing_balance_accumulated_depreciation,

                'net_book': item_net_book
            })
        
        
        ## Redirect to the Tree View or Export Report
        data = self.env['fixed.asset.schedule.report'].search([])
        if data:
            return data.env['report'].get_action(data, 'fixed_asset_report.fixed_asset_schedule_report_template')
        else:
            raise UserError("No data found.")

    
    @api.multi
    def print_fixed_asset_register_report(self, search_month, company_id, currency_id):
        now = datetime.now().date()
        days = calendar.monthrange(now.year,int(search_month))[1]
        search_start_date = datetime(now.year,int(search_month), 1).date().strftime('%Y-%m-%d')
        search_end_date = datetime(now.year,int(search_month), days).date().strftime('%Y-%m-%d')

        
        ## Get Month Name
        months = [ 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'Setember', 'October', 'November', 'December' ]
        month_name = months[int(search_month) - 1]
        month_name = month_name.capitalize()

        
        ## Get Fixed Asset Register
        condition_for_daterange = "AND (aadl.depreciation_date BETWEEN '" + search_start_date + "' AND '" + search_end_date + "')"
        condition_for_daterange_line = "AND (line.depreciation_date BETWEEN '" + search_start_date + "' AND '" + search_end_date + "')"
        self.env.cr.execute(""" SELECT 
                                    aac.id AS category_id
                                    , aaa.id AS asset_id
                                    , aaa.asset_code
                                    , aaa.name AS asset_name
                                    , aaa.manufacturer
                                    , aaa.serial_number
                                    , aaa.model_number
                                    , aaa.create_date AS purchase_date
                                    , aaa.value AS cost
                                    , ( CASE 
                                            WHEN (SELECT sum(line.depreciated_value) FROM account_asset_depreciation_line line LEFT JOIN account_asset_asset asset ON line.asset_id = asset.id WHERE asset.state = 'open' {0} AND asset.id = aaa.id) IS NULL THEN '0'
                                            ELSE (SELECT sum(line.depreciated_value) FROM account_asset_depreciation_line line LEFT JOIN account_asset_asset asset ON line.asset_id = asset.id WHERE asset.state = 'open' {1} AND asset.id = aaa.id)
                                    END ) AS accumulated_depreciation
                                    , ( CASE
                                        WHEN (SELECT sum(line.remaining_value) FROM account_asset_depreciation_line line LEFT JOIN account_asset_asset asset ON line.asset_id = asset.id WHERE asset.state = 'open' {2} AND asset.id = aaa.id) IS NULL THEN '0'
                                        ELSE (SELECT sum(line.remaining_value) FROM account_asset_depreciation_line line LEFT JOIN account_asset_asset asset ON line.asset_id = asset.id WHERE asset.state = 'open' {3} AND asset.id = aaa.id)
                                    END ) AS net_book
                                    , aaa.currency_id
                                    , aaa.company_id
                                FROM account_asset_depreciation_line aadl
                                LEFT JOIN account_asset_asset aaa ON aadl.asset_id = aaa.id
                                LEFT JOIN account_asset_category aac ON aaa.category_id = aac.id
                                WHERE aaa.company_id = 1
                                {4}
                                AND aaa.company_id = %s
                                GROUP BY aaa.id
                                        , aac.id
                                        , aaa.asset_code
                                        , aaa.name
                                        , aaa.manufacturer
                                        , aaa.serial_number
                                        , aaa.model_number
                                        , aaa.create_date
                                        , aaa.currency_id
                                        , aaa.company_id; """.format(
                                                                        condition_for_daterange_line,
                                                                        condition_for_daterange_line,
                                                                        condition_for_daterange_line,
                                                                        condition_for_daterange_line,
                                                                        condition_for_daterange
                                                                    ), (tuple(str(company_id)),))
        res = self.env.cr.dictfetchall()


        ## Clear existing table data
        self.env.cr.execute(""" TRUNCATE TABLE fixed_asset_register_report ; """)

        
        ## Push new data to the table
        for item in res:
            self.env['fixed.asset.register.report'].create({
                'category_id': item['category_id'],
                'asset_id': item['asset_id'],
                'asset_code': item['asset_code'],
                'asset_name': item['asset_name'],
                'manufacturer': item['manufacturer'],
                'serial_number': item['serial_number'],
                'model_number': item['model_number'],
                'purchase_date': item['purchase_date'],
                'cost': item['cost'],
                'accumulated_depreciation': item['accumulated_depreciation'],
                'net_book': item['net_book'],

                'month': month_name,
                'currency_id': currency_id
            })
        
        
        ## Redirect to the Tree View or Export Report
        data = self.env['fixed.asset.register.report'].search([])
        if data:
            return data.env['report'].get_action(data, 'fixed_asset_report.fixed_asset_register_report_template')
        else:
            raise UserError("No data found.")

