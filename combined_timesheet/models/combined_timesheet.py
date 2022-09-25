# -*- coding: utf-8 -*-

from odoo import models, fields, api

class combined_timesheet(models.Model):
    _inherit = 'hr.contract'
    
    def get_late_hours(self,date_from,date_to):
        timesheet = self.env['combined.timesheet'].search([('date_from','<=',date_from),('date_to','>=',date_to),('employee_id','=',self.employee_id.id)])
        return sum([t.late_hours for t in timesheet])
    def get_absence_days(self,date_from,date_to):
        timesheet = self.env['combined.timesheet'].search([('date_from','<=',date_from),('date_to','>=',date_to),('employee_id','=',self.employee_id.id)])
        return sum([t.absence_days for t in timesheet])
    def get_overtime_hours(self,date_from,date_to):
        timesheet = self.env['combined.timesheet'].search([('date_from','<=',date_from),('date_to','>=',date_to),('employee_id','=',self.employee_id.id)])
        return sum([t.overtime_hours for t in timesheet])
    def get_working_days(self,date_from,date_to):
        timesheet = self.env['combined.timesheet'].search([('date_from','<=',date_from),('date_to','>=',date_to),('employee_id','=',self.employee_id.id)])
        return sum([t.working_days for t in timesheet])
    def get_working_hours(self,date_from,date_to):
        timesheet = self.env['combined.timesheet'].search([('date_from','<=',date_from),('date_to','>=',date_to),('employee_id','=',self.employee_id.id)])
        return sum([t.working_days for t in timesheet])
        
class combined_timesheet(models.Model):
    _name = 'combined.timesheet'
    employee_id = fields.Many2one('hr.employee')
    date_from = fields.Date()
    date_to = fields.Date()
    absence_days = fields.Integer()
    overtime_hours = fields.Float()
    late_hours = fields.Float()
    working_days = fields.Integer(compute = '_set_working_days')
    working_hours = fields.Integer(compute = '_set_working_hours')
    
    def get_working_hours(self):
        contract = self.env['hr.contract'].search([('employee_id','=',self.employee_id.id)])
        if not(contract):
            return 0
        return contract.resource_calendar_id.hours_per_day * self.get_working_days()
    def get_working_days(self):
        if not(self.date_from) or not(self.date_to):
            return 0
        return (self.date_to - self.date_from).days
    
    @api.depends('date_from','date_to')
    def _set_working_days(self):
        for rec in self:
            rec.working_days = rec.get_working_days()
    @api.depends('date_from','date_to','employee_id')
    def _set_working_hours(self):
        for rec in self:
            rec.working_hours = rec.get_working_hours()
    
