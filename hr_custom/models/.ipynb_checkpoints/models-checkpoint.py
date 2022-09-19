# -*- coding: utf-8 -*-

from odoo import models, fields, api

class hr_custom_2(models.Model):
    _inherit = 'hr.contract'
    vacetion_days = fields.Float()
    insurance_premuim = fields.Float()
    car_allowance = fields.Float()
    medical_insurance = fields.Float()
    transportation_allowance = fields.Float()
    housing_allowance = fields.Float()
    food_allowance = fields.Float()
    mobile_allowance = fields.Float()
    fuel_allowance = fields.Float()
    other_allowance = fields.Float()
    ticket_allowance = fields.Float()
    commission_allowance = fields.Float()
    telephone_allowance = fields.Float()

    allowance_total = fields.Float(compute = '_set_allowance_total')
    @api.depends('car_allowance','medical_insurance','transportation_allowance','housing_allowance','mobile_allowance','fuel_allowance','other_allowance','ticket_allowance','telephone_allowance')
    def _set_allowance_total(self):
        for rec in self:
            rec.allowance_total = rec.car_allowance + rec.medical_insurance + rec.transportation_allowance + rec.housing_allowance + rec.mobile_allowance + rec.fuel_allowance + rec.other_allowance + rec.ticket_allowance + rec.telephone_allowance  
    eosb = fields.Float('EOSB')
    gosi = fields.Char('GOSI',compute = '_set_gosi',store = True)
    gosi_type = fields.Selection([('national','national'),('foriegn','foriegn')],default = 'national',required = True)
    gosi_percent = fields.Float(compute = '_set_gosi',store = True)
    medical_insurance_type = fields.Selection([('b','B'),('mg2','MG2'),('mg3','MG3'),('mg7','MG7')])
    @api.depends('gosi_type','wage')
    def _set_gosi(self):
        for rec in self:
            rec.gosi_percent = 0.22 if rec.gosi_type == 'national' else 0.02
            rec.gosi = rec.gosi_percent * rec.wage
    ticket = fields.Char()



class hr_custom(models.Model):
    _inherit = 'hr.employee'
    custom_id = fields.Char('ID',readonly = True)
    foriegn_name = fields.Char()
    sponsorship = fields.Selection([('out','خارج الكفالة'),('under','تحت الكفالة')])
    insurance_class = fields.Selection([('b','B'),('mg2','MG2'),('mg3','MG3'),('mg7','MG7')])
    staying = fields.Char('المهنة بالأقامة')
    cost_center_id = fields.Many2one('account.analytic.account')
    project_id = fields.Many2one('project.project')
    gosi = fields.Char('GOSI')
    employee_state = fields.Selection([('active','active'),('Vacation','Vacation'),('Terminated','Terminated'),('Resignation','Resignation'),('End of Contract','End of Contract')])
    border_no = fields.Char()
    no_of_dependance = fields.Char()
    def message_helper(self,body):
        vals = {
             'email_from': self.env.user.partner_id.email, # add the sender email
             'author_id': self.env.user.partner_id.id, # add the creator id
             'subtype_id': self.env.ref('mail.mt_comment').id, #Leave this as it is
             'body': body, # here add the message body
            'record_name' : self.name,
            'model' : 'hr.employee',
            'res_id' : self.id,
            'message_type': 'comment'
          }        
        m = self.env['mail.message'].create(vals)
    @api.constrains('visa_expire')
    def track_1(self):
        for rec in self:
            rec.message_helper(f'visa number is set to {rec.visa_expire}')
    @api.constrains('project_id')
    def track_2(self):
        for rec in self:
            rec.message_helper(f'project is set to {rec.project_id.name}')
    @api.constrains('cost_center_id')
    def track_3(self):
        for rec in self:
            rec.message_helper(f'cost center is set to {rec.cost_center_id.name}')
    @api.model
    def create(self,vals):
        res = super().create(vals)
        res.custom_id = res.company_id.prefix + '-' + str(res.id)
        return res
        
