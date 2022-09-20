#!/usr/bin/python
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning


class Partner(models.Model):
    _name = "res.partner"
    _inherit = "res.partner"
    building_no = fields.Char(string="Building no", help="Building No")
    district = fields.Char(string="District", help="District")
    code = fields.Char(string="Code", help="Code")
    additional_no = fields.Char(string="Additional no", help="Additional No")
    other_id = fields.Char(string="Other ID", help="Other ID")
#     company_id = fields.Many2one(default = lambda self : self.env.company.id)
    foreign_name = fields.Char(string="Foreign Name", help="Foreign Name")
    partner_number = fields.Char(string="Client No.", help="Client No.",readonly = True)
    contact_person = fields.Char(string="Contact Person", help="Contact Person")
    
    @api.constrains('company_id')
    def set_sequence(self):
        for rec in self:
            rec.partner_number = (self.env['ir.sequence'].next_by_code(rec.company_id.sequence_id.code)) or 'New'
    def test(self):
        pass
