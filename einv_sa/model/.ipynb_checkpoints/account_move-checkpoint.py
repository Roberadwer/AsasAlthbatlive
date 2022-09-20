#!/usr/bin/python
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import base64
from odoo.exceptions import UserError, Warning
class AccountMoveAA(models.Model):
    _inherit = "account.analytic.group"
    code_2 = fields.Char('Code')
class AccountMoveA(models.Model):
    _inherit = "account.analytic.account"
    code_2 = fields.Char('Code')

class AccountMove(models.Model):
    _name = "account.move"
    _inherit = "account.move"

    einv_amount_sale_total = fields.Monetary(string="Amount sale total", compute="_compute_total", store='True',
                                             help="")
    einv_amount_discount_total = fields.Monetary(string="Amount discount total", compute="_compute_total", store='True',
                                                 help="")
    einv_amount_tax_total = fields.Monetary(string="Amount tax total", compute="_compute_total", store='True', help="")

    # amount_invoiced = fields.Float(string="Amount tax total", help="")
    # qrcode = fields.Char(string="QR", help="")

    project_code = fields.Char(string="Project Code/Sales Order", help="Project Code / Sales Order")
    project_name = fields.Char(string="Project name", help="Project name")
    purchase_order = fields.Char(string="P.O #", help="P.O #:")
    contract_no = fields.Char(string="Contract No.", help="Contract Number")
    quotation_no = fields.Char(string="Quotation No.", help="Quotation Number")
    invoice_period = fields.Date()
    qr_code_str = fields.Char(string='Zatka QR Code', compute='_compute_qr_code_str')
    confirmation_datetime = fields.Datetime(string='Confirmation Date', readonly=False, copy=False)
    show_delivery_date = fields.Boolean(compute='_compute_show_delivery_date')

    @api.depends('country_code', 'move_type')
    def _compute_show_delivery_date(self):
        for move in self:
            move.show_delivery_date = move.move_type in ('out_invoice', 'out_refund')

    def action_post(self):
        res = super(AccountMove, self).action_post()
        for record in self:
            if record.move_type in ('out_invoice', 'out_refund'):
                if not record.show_delivery_date:
                    raise UserError(_('Delivery Date cannot be empty'))

                self.write({
                    'confirmation_datetime': fields.Datetime.now()
                })
        return res

    @api.depends('amount_total', 'amount_untaxed', 'confirmation_datetime', 'company_id', 'company_id.vat')
    def _compute_qr_code_str(self):
        def get_qr_encoding(tag, field):
            company_name_byte_array = field.encode('UTF-8')
            company_name_tag_encoding = tag.to_bytes(length=1, byteorder='big')
            company_name_length_encoding = len(company_name_byte_array).to_bytes(length=1, byteorder='big')
            text = company_name_tag_encoding + company_name_length_encoding + company_name_byte_array
            print(text)
            return company_name_tag_encoding + company_name_length_encoding + company_name_byte_array

        for record in self:
            print('mmmmm')
            qr_code_str = ''
            if record.confirmation_datetime and record.company_id.vat:
                seller_name_enc = get_qr_encoding(1, record.company_id.name)
                company_vat_enc = get_qr_encoding(2, record.company_id.vat)
                time_sa = fields.Datetime.context_timestamp(self.with_context(tz='Asia/Riyadh'),
                                                            record.confirmation_datetime)
                timestamp_enc = get_qr_encoding(3, time_sa.isoformat())
                # timestamp_enc = get_qr_encoding(3, self.confirmation_datetime.isoformat()[:19] + 'Z')
                invoice_total_enc = get_qr_encoding(4, str(record.amount_total))
                total_vat_enc = get_qr_encoding(5, str(record.currency_id.round(
                    record.amount_total - record.amount_untaxed)))
                test = self.confirmation_datetime.isoformat()[:19] + 'Z'
                print(test)
                print(timestamp_enc)
                str_to_encode = seller_name_enc + company_vat_enc + timestamp_enc + invoice_total_enc + total_vat_enc
                qr_code_str = base64.b64encode(str_to_encode).decode('UTF-8')
                print(qr_code_str)
            record.qr_code_str = qr_code_str

    @api.depends('invoice_line_ids', 'amount_total')
    def _compute_total(self):
        for r in self:
            r.einv_amount_sale_total = r.amount_untaxed + sum(line.einv_amount_discount for line in r.invoice_line_ids)
            r.einv_amount_discount_total = sum(line.einv_amount_discount for line in r.invoice_line_ids)
            r.einv_amount_tax_total = sum(line.einv_amount_tax for line in r.invoice_line_ids)

    def _compute_amount(self):
        res = super(AccountMove, self)._compute_amount()

        # do the things here
        return res


class AccountMoveLine(models.Model):
    _name = "account.move.line"
    _inherit = "account.move.line"

    einv_amount_discount = fields.Monetary(string="Amount discount", compute="_compute_amount_discount", store='True',
                                           help="")
    einv_amount_tax = fields.Monetary(string="Amount tax", compute="_compute_amount_tax", store='True', help="")

    # product_unitom_id = fields.Many2one('unitom.unitom', "Unit of Measure", related="product_id.product_unitom_id")
    product_unitom_id = fields.Many2one('unitom.unitom', "Unit of Measure")

    @api.depends('discount', 'quantity', 'price_unit')
    def _compute_amount_discount(self):
        for r in self:
            r.einv_amount_discount = r.quantity * r.price_unit * (r.discount / 100)

    @api.depends('tax_ids', 'discount', 'quantity', 'price_unit')
    def _compute_amount_tax(self):
        for r in self:
            r.einv_amount_tax = sum(r.price_subtotal * (tax.amount / 100) for tax in r.tax_ids)


class UnitoM(models.Model):
    _name = 'unitom.unitom'
    _description = 'Product Unit of Measure'
    _order = "name"

    name = fields.Char('Unit of Measure', required=True)


class Product(models.Model):
    _inherit = "product.product"

    product_unitom_id = fields.Many2one('unitom.unitom', "Unit of Measure")


class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_unitom_id = fields.Many2one('unitom.unitom', "Unit of Measure")

#
# class Bank(models.Model):
#     _inherit = 'res.bank'
#
#     company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)