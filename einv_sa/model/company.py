#!/usr/bin/python
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning


class Company(models.Model):
    _name = "res.company"
    _inherit = "res.company"

    building_no = fields.Char(string="Building no", related='partner_id.building_no', help="Building No")
    district = fields.Char(string="District", related='partner_id.district', help="District")
    code = fields.Char(string="Code", related='partner_id.code', help="Code")
    additional_no = fields.Char(string="Additional no", related='partner_id.additional_no', help="Additional No")
    other_id = fields.Char(string="Other ID", related='partner_id.other_id', help="")

    foreign_name = fields.Char(string="Foreign Name", help="Foreign Name")
    bank_id = fields.Many2one('res.bank', string='Bank')
    
    beneficiary = fields.Char()
    bank_name = fields.Char()
    account_nubmer = fields.Char()
    iban = fields.Char()
    
    #sequence
    sequence_code = fields.Char()
    sequence_id = fields.Many2one('ir.sequence')
    
    @api.constrains('sequence_code')
    def create_company_sequence(self):
        for rec in self:
            if rec.sequence_code:
                sequence = self.env['ir.sequence'].create({
                    'name' : rec.name + ' sequence',
                    'code' : f'company.sequence.{rec.sequence_code}',
                    'company_id' : rec.id,
                    'padding' : 7,
                    'prefix' : f'{rec.sequence_code}',
                    'number_next_actual' : 1,
                 })
                rec.sequence_id = sequence.id