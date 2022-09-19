# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class hr_contract_inherit(models.Model):
    _inherit = 'hr.contract'

    end_of_contract = fields.Boolean(string="End Of Contract ?", default='false')

    reason_of_ending_contract = fields.Selection(string="Reason Of Ending Contract",
                                                 selection=[('termination', 'Termination')],
                                                 required=False, )