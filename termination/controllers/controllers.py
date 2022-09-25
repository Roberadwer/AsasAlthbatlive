# -*- coding: utf-8 -*-
# from odoo import http


# class Termination(http.Controller):
#     @http.route('/termination/termination/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/termination/termination/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('termination.listing', {
#             'root': '/termination/termination',
#             'objects': http.request.env['termination.termination'].search([]),
#         })

#     @http.route('/termination/termination/objects/<model("termination.termination"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('termination.object', {
#             'object': obj
#         })
