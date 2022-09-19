# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import Warning, ValidationError
from datetime import date, datetime


class HREmployeesTermination(models.Model):
    _name = 'hr.termination'

    name = fields.Char(compute='_set_name')

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, )

    termination_type = fields.Selection(string="",
                                        selection=[('end_of_service_1', 'نهاية عقد'),
                                                   ('end_of_service_2', 'فسخ عقد بالتراضي'), ('terminate', 'فصل'),
                                                   ('resignation', 'إستقاله'), ], required=False, )

    state = fields.Selection(string="", selection=[('draft', 'draft'),('confirm', 'Confirmed')], required=False,
                             default='draft')

    # TODO NEW WORKFLOW



    def accounting_2_confirm(self):
        for rec in self:
            rec.state = 'confirm'
            self.create_account_move()

    def reject(self):
        self.state = 'rejected'

    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')

    @api.constrains('state')
    def _check_attachment(self):
        for record in self:
            if record.state == 'confirm':
                if not self.attachment_ids:
                    raise ValidationError(_('You cannot send the termination request without attaching a document.'))

    @api.constrains('last_working_days')
    def _check_last_working_days(self):
        for record in self:
            if record.last_working_days > 30:
                self.last_working_days = 30
                # raise ValidationError(_('Your Last Working Days Cant be more than 30.'))

    employee_company_id = fields.Many2one('res.company', readonly=True, )

    employee_department_id = fields.Many2one('hr.department', related='employee_id.department_id')


    joining_date = fields.Date(readonly=True, related='employee_id.joining_date')

    line_ids = fields.One2many('hr.termination.approvals', 'termination_id', "Approvals", readonly=True)
    notes = fields.Text()

    approved = fields.Boolean(string="", default=False)

    contract_id = fields.Many2one('hr.contract', related='employee_id.contract_id')
    contract_joining_date = fields.Date(readonly=True, related='contract_id.date_start')
    today_date = fields.Date(readonly=True, default=fields.Date.context_today)
    duration_days = fields.Float(string="Duration/days", store=False, compute="_get_contract_months")
    duration = fields.Float(string="Duration/years", store=False, compute="_get_contract_months")
    indemnity = fields.Float(string="Total EOS", required=False, compute="_get_indemnity_value")

    refundable_advance = fields.Float(string="A refundable advance", required=False, readonly=True)
    refundable_bonus = fields.Float(string="A Refundable Bonus", required=False, readonly=True, )
    other_allowances = fields.Float(string="Other Allowances", required=False, compute="get_new_other_allowances")
    new_other_allowances = fields.Float(string="Other Allowances", required=False, )
    other_deductions = fields.Float(string="Other Deductions", required=False, compute="get_new_other_deductions")
    new_other_deductions = fields.Float(string="Other Deductions", required=False, )

    allowance_amount = fields.Float(string="", required=False, )

    saudi = fields.Boolean(string="EXCEPTION", )
    accounting_method = fields.Boolean(string="", )
    left_vacation_days = fields.Float(string="", required=False, )
    left_vacation_amount = fields.Float(string="", required=False, )
    wage_day_amount = fields.Float(string="", required=False, )

    journal_id = fields.Many2one(comodel_name="account.journal", string="", )
    debit_account_id = fields.Many2one(comodel_name="account.account", string="", )
    credit_account_id = fields.Many2one(comodel_name="account.account", string="", )
    account_move_id = fields.Many2one(comodel_name="account.move", string="", )
    outstanding_loans = fields.Float(string="", required=False, )

    last_working_day = fields.Date(string="", required=False, )
    last_working_days = fields.Float(string="", required=False, store=True)
    deserved_salary = fields.Float(string="", required=False, compute="_get_deserved_salary")

    comprehensive_wage = fields.Float(string="", required=False, )
    day_amount = fields.Float(string="", required=False, )
    total = fields.Float(string="", required=False, compute="_get_total")

    left_vacation_amount_journal_id = fields.Many2one(comodel_name="account.journal", string="", )
    left_vacation_amount_debit_account_id = fields.Many2one(comodel_name="account.account", string="", )
    left_vacation_amount_credit_account_id = fields.Many2one(comodel_name="account.account", string="", )
    left_vacation_amount_account_move_id = fields.Many2one(comodel_name="account.move", string="", )

    deserved_salary_journal_id = fields.Many2one(comodel_name="account.journal", string="", )
    deserved_salary_debit_account_id = fields.Many2one(comodel_name="account.account", string="", )
    deserved_salary_credit_account_id = fields.Many2one(comodel_name="account.account", string="", )
    deserved_salary_move_id = fields.Many2one(comodel_name="account.move", string="", )

    outstanding_loans_journal_id = fields.Many2one(comodel_name="account.journal", string="", )
    outstanding_loans_debit_account_id = fields.Many2one(comodel_name="account.account", string="", )
    outstanding_loans_credit_account_id = fields.Many2one(comodel_name="account.account", string="", )
    outstanding_loans_move_id = fields.Many2one(comodel_name="account.move", string="", )

    absence_days = fields.Float(string="Absence Days", required=False, )
    new_absence_days_deduction = fields.Float(string="Absence Days Deduction", required=False, )
    absence_days_deduction = fields.Float(string="Absence Days Deduction", required=False,
                                          compute="get_absence_days_deduction")

    absence_days_journal_id = fields.Many2one(comodel_name="account.journal", string="", )
    absence_days_debit_account_id = fields.Many2one(comodel_name="account.account", string="", )
    absence_days_credit_account_id = fields.Many2one(comodel_name="account.account", string="", )
    absence_days_move_id = fields.Many2one(comodel_name="account.move", string="", )

    other_allowances_journal_id = fields.Many2one(comodel_name="account.journal", string="", )
    other_allowances_debit_account_id = fields.Many2one(comodel_name="account.account", string="", )
    other_allowances_credit_account_id = fields.Many2one(comodel_name="account.account", string="", )
    other_allowances_move_id = fields.Many2one(comodel_name="account.move", string="", )

    other_deductions_journal_id = fields.Many2one(comodel_name="account.journal", string="", )
    other_deductions_debit_account_id = fields.Many2one(comodel_name="account.account", string="", )
    other_deductions_credit_account_id = fields.Many2one(comodel_name="account.account", string="", )
    other_deductions_move_id = fields.Many2one(comodel_name="account.move", string="", )

    indemnity_journal_id = fields.Many2one(comodel_name="account.journal", string="", )
    indemnity_debit_account_id = fields.Many2one(comodel_name="account.account", string="", )
    indemnity_credit_account_id = fields.Many2one(comodel_name="account.account", string="", )
    indemnity_move_id = fields.Many2one(comodel_name="account.move", string="", )

    final_total = fields.Float(string="", required=False, compute="get_final_total")
    cancel_deserved_salary = fields.Boolean(string="", default=False)
    sales_person = fields.Many2one('res.users', string='Sales Person', default=lambda self: self.env.uid,
                                   track_visibility='always')

    @api.depends('employee_id', 'deserved_salary', 'left_vacation_amount', 'other_allowances', 'other_deductions',
                 'new_absence_days_deduction', 'outstanding_loans')
    def get_final_total(self):
        if self.employee_id:
            self.final_total = self.deserved_salary + self.left_vacation_amount + self.other_allowances + self.indemnity - self.other_deductions - self.new_absence_days_deduction - self.outstanding_loans
        else:
            self.final_total = 0.0

    @api.depends('new_absence_days_deduction', 'day_amount', 'absence_days')
    def get_absence_days_deduction(self):
        if self.employee_id and self.absence_days:
            self.absence_days_deduction = self.absence_days * self.day_amount
            self.new_absence_days_deduction = self.absence_days * self.day_amount
        else:
            self.absence_days_deduction = 0.0
            self.new_absence_days_deduction = 0.0

    @api.onchange('new_absence_days_deduction', 'absence_days', 'day_amount')
    def get_absence_days_deduction(self):

        if self.employee_id and self.absence_days:
            self.absence_days_deduction = self.absence_days * self.day_amount
            self.new_absence_days_deduction = self.absence_days * self.day_amount
        else:
            self.absence_days_deduction = 0.0
            self.new_absence_days_deduction = 0.0

    @api.depends('last_working_days', 'day_amount', 'employee_id', 'contract_id')
    def _get_deserved_salary(self):
        if self.last_working_days and self.day_amount:
            self.deserved_salary = self.last_working_days * self.day_amount
            print(">>>>>>>>>>>>>>>>>", self.deserved_salary)
        else:
            self.deserved_salary = 0.0

    @api.depends('joining_date', 'last_working_day')
    def _get_contract_months(self):
        if self.last_working_day and self.joining_date:
            num_days = self.last_working_day - self.joining_date
            num_days = num_days.days
            num_years = num_days / 365
            self.duration_days = num_days
            self.duration = num_years
        else:
            self.duration_days = 0.0
            self.duration = 0.0


    @api.onchange('termination_type', 'other_deductions', 'other_allowances', 'last_working_day', 'saudi',
                  'absence_days', 'new_absence_days_deduction', 'cancel_deserved_salary', 'indemnity',
                  'deserved_salary')
    def _get_indemnity_value(self):
        if self.last_working_day:
            date_from = datetime.strptime(self.last_working_day.strftime('%Y%m%d'), '%Y%m%d')
            self.last_working_days = date_from.day
        telt = 1 / 3
        telten = 2 / 3
        tot_wage = self.contract_id.wage
        if self.duration and self.today_date and self.joining_date and self.termination_type == 'end_of_service_1' or self.termination_type == 'end_of_service_2':
            if self.duration >= 2 and self.duration <= 5:
                print("end_of_service and duration .... self.duration >= 2 and self.duration <= 5")
                total3 = tot_wage * (self.duration / 2)
                total4 = total3 - self.refundable_advance
                if self.saudi == True:
                    self.indemnity = total4
                    if self.cancel_deserved_salary == True:
                        # self.indemnity -= self.deserved_salary
                        self.deserved_salary = 0

                if self.saudi == False:
                    if total4 < 20000:
                        self.indemnity = total4
                    if total4 > 20000:
                        self.indemnity
                    if self.cancel_deserved_salary == True:
                        # self.indemnity -= self.deserved_salary
                        self.deserved_salary = 0

            elif self.duration > 5:
                the_remaining_years = self.duration - 5
                print(the_remaining_years)
                total3 = (tot_wage * (5 / 2)) + (tot_wage * (the_remaining_years))
                total4 = total3 - self.refundable_advance
                if self.saudi == True:
                    self.indemnity = total4
                    if self.cancel_deserved_salary == True:
                        # self.indemnity -= self.deserved_salary
                        self.deserved_salary = 0

                if self.saudi == False:
                    if total4 < 20000:
                        self.indemnity = total4
                    if total4 > 20000:
                        self.indemnity = 20000
                        if self.cancel_deserved_salary == True:
                            # self.indemnity -= self.deserved_salary
                            self.deserved_salary = 0

            elif self.duration < 2:
                print("end_of_service and duration < 2")
                print("terminate   مش هياخد")
                self.indemnity = 0.033333


        elif self.duration and self.today_date and self.joining_date and self.termination_type == 'terminate':
            print("terminate   مش هياخد")
            self.indemnity = 0.0

        elif self.duration and self.today_date and self.joining_date and self.termination_type == 'resignation':
            if self.duration < 2 and self.saudi == False:
                print("resignation and duration < 2   مش هياخد")
                self.indemnity = 0.0
            elif self.duration >= 2 and self.duration < 5 and self.saudi == False:
                print("resignation and duration < 5   هياخد الثلث")
                the_remaining_years = self.duration - 5
                print(the_remaining_years)
                total3 = (tot_wage * (5 / 2)) + (tot_wage * (the_remaining_years))
                total4 = total3 - self.refundable_advance
                if self.saudi == True:
                    self.indemnity = total4
                    if self.cancel_deserved_salary == True:
                        # self.indemnity -= self.deserved_salary
                        self.deserved_salary = 0

                if self.saudi == False:
                    if total4 < 20000:
                        self.indemnity = total4 * telt
                    if total4 > 20000:
                        self.indemnity = 20000
                        if self.cancel_deserved_salary == True:
                            # self.indemnity -= self.deserved_salary
                            self.deserved_salary = 0
            elif self.duration >= 5 and self.duration < 10 and self.saudi == False:
                print("resignation and duration < 10 and not saudi    هياخد الثلثين")
                the_remaining_years = self.duration - 5
                print(the_remaining_years)
                total3 = (tot_wage * (5 / 2)) + (tot_wage * (the_remaining_years))
                total4 = total3 - self.refundable_advance
                if self.saudi == True:
                    self.indemnity = total4
                    if self.cancel_deserved_salary == True:
                        # self.indemnity -= self.deserved_salary
                        self.deserved_salary = 0

                if self.saudi == False:
                    if total4 < 20000:
                        self.indemnity = total4 * telten
                    if total4 > 20000:
                        self.indemnity = 20000
                        if self.cancel_deserved_salary == True:
                            # self.indemnity -= self.deserved_salary
                            self.deserved_salary = 0

            elif self.duration >= 10:
                print("resignation and duration > 10    هياخد كامل")
                the_remaining_years = self.duration - 5
                print(the_remaining_years)
                total3 = (tot_wage * (5 / 2)) + (tot_wage * (the_remaining_years))
                total4 = total3 - self.refundable_advance
                if self.saudi == True:
                    self.indemnity = total4
                    if self.cancel_deserved_salary == True:
                        # self.indemnity -= self.deserved_salary
                        self.deserved_salary = 0

                if self.saudi == False:
                    if total4 < 20000:
                        self.indemnity = total4
                    if total4 > 20000:
                        self.indemnity = 20000
                        if self.cancel_deserved_salary == True:
                            # self.indemnity -= self.deserved_salary
                            self.deserved_salary = 0

        else:
            self.indemnity = 0.0

    ###########################################################################################################
    @api.depends('new_other_allowances')
    def get_new_other_allowances(self):
        if self.new_other_allowances:
            self.other_allowances = self.new_other_allowances
        else:
            self.other_allowances = 0.0

    @api.onchange('new_other_allowances')
    def get_new_other_allowances(self):
        if self.new_other_allowances:
            self.other_allowances = self.new_other_allowances
        else:
            self.other_allowances = 0.0

    ###########################################################################################################
    @api.depends('new_other_deductions')
    def get_new_other_deductions(self):
        if self.new_other_deductions:
            self.other_deductions = self.new_other_deductions
        else:
            self.other_deductions = 0.0

    @api.onchange('new_other_deductions')
    def get_new_other_deductions(self):
        if self.new_other_deductions:
            self.other_deductions = self.new_other_deductions
        else:
            self.other_deductions = 0.0


    def create_account_move(self):

        move_line_3 = {
            'name': self.name or '',
            'account_id': self.left_vacation_amount_debit_account_id.id,
            'debit': self.left_vacation_amount,
            'credit': 0.0,
        }
        print("move_line_3 >>>>>>>>>>", move_line_3)

        move_line_33 = {
            'name': self.name or '',
            'account_id': self.left_vacation_amount_credit_account_id.id,
            'debit': 0.0,
            'credit': self.left_vacation_amount,
        }
        print("move_line_33 >>>>>>>>>>", move_line_33)

        move_vals = {
            'name': self.name or '',
            'date': self.today_date or False,
            'state': 'draft',
            'journal_id': self.left_vacation_amount_journal_id.id,
            'termination_id': self.id,
            'line_ids': [(0, 0, move_line_3), (0, 0, move_line_33)],
        }

        print("move_vals >>>>>>>>>>", move_vals)
        account_move = self.env['account.move'].create(move_vals)
        self.left_vacation_amount_account_move_id = account_move.id

        move_line_5 = {
            'name': self.name or '',
            'account_id': self.deserved_salary_debit_account_id.id,
            'debit': self.deserved_salary,
            'credit': 0.0,
        }
        print("move_line_5 >>>>>>>>>>", move_line_5)

        move_line_55 = {
            'name': self.name or '',
            'account_id': self.deserved_salary_credit_account_id.id,
            'debit': 0.0,
            'credit': self.deserved_salary,
        }
        print("move_line_55 >>>>>>>>>>", move_line_55)
        move_vals = {
            'name': self.name or '',
            'date': self.today_date or False,
            'state': 'draft',
            'journal_id': self.deserved_salary_journal_id.id,
            'termination_id': self.id,
            'line_ids': [(0, 0, move_line_5), (0, 0, move_line_55)],
        }
        print("move_vals >>>>>>>>>>", move_vals)
        account_move = self.env['account.move'].create(move_vals)
        self.deserved_salary_move_id = account_move.id

        move_line_6 = {
            'name': self.name or '',
            'account_id': self.outstanding_loans_credit_account_id.id,
            'debit': 0.0,
            'credit': self.outstanding_loans,
        }
        print("move_line_6 >>>>>>>>>>", move_line_6)

        move_line_66 = {
            'name': self.name or '',
            'account_id': self.outstanding_loans_debit_account_id.id,
            'debit': self.outstanding_loans,
            'credit': 0.0,
        }
        print("move_line_66 >>>>>>>>>>", move_line_66)

        move_vals = {
            'name': self.name or '',
            'date': self.today_date or False,
            'state': 'draft',
            'journal_id': self.outstanding_loans_journal_id.id,
            'termination_id': self.id,
            'line_ids': [(0, 0, move_line_6), (0, 0, move_line_66)],
        }
        print("move_vals >>>>>>>>>>", move_vals)
        account_move = self.env['account.move'].create(move_vals)
        self.outstanding_loans_move_id = account_move.id

        move_line_7 = {
            'name': self.name or '',
            'account_id': self.absence_days_credit_account_id.id,
            'debit': 0.0,
            'credit': self.new_absence_days_deduction,
        }
        print("move_line_7 >>>>>>>>>>", move_line_7)
        move_line_77 = {
            'name': self.name or '',
            'account_id': self.absence_days_debit_account_id.id,
            'debit': self.new_absence_days_deduction,
            'credit': 0.0,
        }
        print("move_line_77 >>>>>>>>>>", move_line_77)
        move_vals = {
            'name': self.name or '',
            'date': self.today_date or False,
            'state': 'draft',
            'journal_id': self.absence_days_journal_id.id,
            'termination_id': self.id,
            'line_ids': [(0, 0, move_line_7), (0, 0, move_line_77)],
        }
        print("move_vals >>>>>>>>>>", move_vals)
        account_move = self.env['account.move'].create(move_vals)
        self.absence_days_move_id = account_move.id

        move_line_8 = {
            'name': self.name or '',
            'account_id': self.other_allowances_credit_account_id.id,
            'debit': 0.0,
            'credit': self.other_allowances,
        }
        print("move_line_8 >>>>>>>>>>", move_line_8)
        move_line_88 = {
            'name': self.name or '',
            'account_id': self.other_allowances_debit_account_id.id,
            'debit': self.other_allowances,
            'credit': 0.0,
        }
        print("move_line_88 >>>>>>>>>>", move_line_88)
        move_vals = {
            'name': self.name or '',
            'date': self.today_date or False,
            'state': 'draft',
            'journal_id': self.other_allowances_journal_id.id,
            'termination_id': self.id,
            'line_ids': [(0, 0, move_line_8), (0, 0, move_line_88)],
        }
        print("move_vals >>>>>>>>>>", move_vals)
        account_move = self.env['account.move'].create(move_vals)
        self.other_allowances_move_id = account_move.id
        # ///////////////////////////////////////////////////////////////////////////////////////////////////
        move_line_9 = {
            'name': self.name or '',
            'account_id': self.other_deductions_credit_account_id.id,
            'debit': 0.0,
            'credit': self.other_deductions,

        }
        print("move_line_9 >>>>>>>>>>", move_line_9)
        move_line_99 = {
            'name': self.name or '',
            'account_id': self.other_deductions_debit_account_id.id,
            'debit': self.other_deductions,
            'credit': 0.0,
        }
        print("move_line_99 >>>>>>>>>>", move_line_99)
        move_vals = {
            'name': self.name or '',
            'date': self.today_date or False,
            'state': 'draft',
            'journal_id': self.other_deductions_journal_id.id,
            'termination_id': self.id,
            'line_ids': [(0, 0, move_line_9), (0, 0, move_line_99)],
        }
        print("move_vals >>>>>>>>>>", move_vals)
        account_move = self.env['account.move'].create(move_vals)
        self.other_deductions_move_id = account_move.id

        move_line_4 = {
            'name': self.name or '',
            'account_id': self.indemnity_credit_account_id.id,
            'debit': 0.0,
            'credit': self.indemnity,

        }
        print("move_line_4 >>>>>>>>>>", move_line_4)
        move_line_44 = {
            'name': self.name or '',
            'account_id': self.indemnity_debit_account_id.id,
            'debit': self.indemnity,
            'credit': 0.0,
        }
        print("move_line_44 >>>>>>>>>>", move_line_44)
        move_vals = {
            'name': self.name or '',
            'date': self.today_date or False,
            'state': 'draft',
            'journal_id': self.indemnity_journal_id.id,
            'termination_id': self.id,
            'line_ids': [(0, 0, move_line_4), (0, 0, move_line_44)],
        }
        print("move_vals >>>>>>>>>>", move_vals)
        account_move = self.env['account.move'].create(move_vals)
        self.indemnity_move_id = account_move.id
        # ///////////////////////////////////////////////////////////////////////////////////////////////////

    @api.depends('wage_day_amount', 'duration')
    def _get_total(self):
        if self.wage_day_amount and self.duration:
            self.total = self.wage_day_amount * self.duration
        else:
            self.total = 0.0

    @api.onchange('employee_id')
    def set_employee_info(self):
        self._get_indemnity_value()
        if self.employee_id:
            loan_obj = self.env['hr.loan'].search([('employee_id', '=', self.employee_id.id), ])
            if loan_obj:
                total = 0.0
                for loan in loan_obj:
                    loan_ids = loan.loan_lines.filtered(lambda x: not x.paid)
                    total += sum(loan_ids.mapped('amount'))
                self.outstanding_loans = total
            if not loan_obj:
                self.outstanding_loans = 0.0
            total = 0.0
            total_days = self.env['hr.leave.report'].search(
                [('employee_id', '=', self.employee_id.id), ('state', '=', 'validate')])
            self.comprehensive_wage = self.employee_id.contract_id.wage
            self.wage_day_amount = self.employee_id.contract_id.wage / 30
            for days in total_days:
                total += days.number_of_days
            self.left_vacation_days = total
            self.day_amount = self.employee_id.contract_id.wage / 30
            self.left_vacation_amount = total * self.day_amount

            self.employee_company_id = self.employee_id.company_id.id
            contracts = self.env['hr.contract'].search(
                [('employee_id', '=', self.employee_id.id), ('state', '=', 'open')])
            if len(contracts) > 0:
                self.employee_company_id = contracts[0].company_id.id
        else:
            self.employee_company_id = False
            self.refundable_advance = 0.0
            self.refundable_bonus = 0.0

    @api.constrains('employee_id')
    def survey_id_constrains(self):
        if self.employee_id:
            self.comprehensive_wage = self.employee_id.contract_id.wage
            self.day_amount = self.employee_id.contract_id.wage / 30
            if self.last_working_day:
                date_from = datetime.strptime(self.last_working_day.strftime('%Y%m%d'), '%Y%m%d')
                self.last_working_days = date_from.day
            elif not self.last_working_day:
                self.last_working_days = False
            loan_obj = self.env['hr.loan'].search([('employee_id', '=', self.employee_id.id), ])
            if loan_obj:
                total = 0.0
                for loan in loan_obj:
                    loan_ids = loan.loan_lines.filtered(lambda x: not x.paid)
                    print(loan_obj)
                    total += sum(loan_ids.mapped('amount'))
                self.outstanding_loans = total
            if not loan_obj:
                self.outstanding_loans = 0.0

            total = 0.0
            total_days = self.env['hr.leave.report'].search(
                [('employee_id', '=', self.employee_id.id), ('state', '=', 'validate')])
            self.comprehensive_wage = self.employee_id.contract_id.wage
            self.wage_day_amount = self.employee_id.contract_id.wage / 30
            for days in total_days:
                total += days.number_of_days
            self.left_vacation_days = total
            self.day_amount = self.employee_id.contract_id.wage / 30
            self.left_vacation_amount = total * self.day_amount

            same_employee_count = self.env['hr.termination'].search_count([('employee_id', '=', self.employee_id.id)])
            if same_employee_count > 1:
                raise ValidationError(_('Employee must be unique'))

    @api.depends('employee_id')
    def _set_name(self):
        for rec in self:
            if rec.employee_id:
                rec.name = rec.employee_id.name + "'s Termination"
            else:
                rec.name = ''



class HREmployeesEvaluationQuestions(models.Model):
    _name = 'hr.termination.approvals'
    termination_id = fields.Many2one('hr.termination')
    user_id = fields.Many2one('res.users', required=True)
    date_of_approval = fields.Date()


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    joining_date = fields.Date(readonly=False, )
