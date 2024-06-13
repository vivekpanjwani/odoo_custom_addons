# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import binascii

from odoo import fields, http, SUPERUSER_ID, _
from odoo.exceptions import AccessError, MissingError, ValidationError
from odoo.fields import Command
from odoo.http import request
from collections import OrderedDict
from operator import itemgetter
from odoo.tools import date_utils, groupby as groupbyelem
from odoo.osv.expression import AND, OR

from odoo.addons.payment.controllers import portal as payment_portal
from odoo.addons.payment import utils as payment_utils
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager

class EmployeeForm(http.Controller):

    @http.route('/employee_webform', type="http", auth="public", website=True)
    def employee_webform(self, **kw):
        country_rec = request.env['res.country'].sudo().search([])
        state_rec = request.env['res.country.state'].sudo().search([])
        city_rec = request.env['city.city'].sudo().search([])
        return http.request.render('emp.employee_form', {
            'country_rec': country_rec,
            'state_rec': state_rec,
            'city_rec': city_rec,
            'employee_rec': None,
        })

    @http.route('/create/webemployee', type="http", auth="public", website=True)
    def create_webemployee(self, **kw):
        employee_vals = {
            'name': kw.get('name'),
            'dob': kw.get('dob'),
            'email': kw.get('email'),
            'street': kw.get('street'),
            'street2': kw.get('street2'),
            'city': kw.get('city'),
            'state_id': kw.get('state_id'),
            'country_id': kw.get('country_id'),
        }
        request.env['emp.model'].sudo().create(employee_vals)
        return request.render('emp.employee_success', {})

    @http.route('/edit/webemployee/<int:employee_id>', type="http", auth="public", website=True, methods=['GET'])
    def edit_webemployee(self, employee_id, **kw):
        employee_rec = request.env['emp.model'].sudo().browse(employee_id)
        country_rec = request.env['res.country'].sudo().search([])
        state_rec = request.env['res.country.state'].sudo().search([])
        city_rec = request.env['city.city'].sudo().search([])

        return http.request.render('emp.employee_form', {
            'employee_rec': employee_rec,
            'country_rec': country_rec,
            'state_rec': state_rec,
            'city_rec': city_rec,
        })

    @http.route('/update/webemployee/<int:employee_id>', type="http", auth="public", website=True, methods=['POST'])
    def update_webemployee(self, employee_id, **kw):
        print(kw)
        if request.env.user.has_group('base.group_user') or request.env.user.has_group('base.group_portal'):
            employee_rec = request.env['emp.model'].sudo().browse(employee_id)
            employee_vals = {
                'name': kw.get('name'),
                'dob': kw.get('dob'),
                'email': kw.get('email'),
                'street': kw.get('street'),
                'street2': kw.get('street2'),
                'city': int(kw.get('city')) if kw.get('city') else False,
                'state_id': int(kw.get('state_id')) if kw.get('state_id') else False,
                'country_id': int(kw.get('country_id')) if kw.get('country_id') else False,
                    }
            employee_rec.sudo().write(employee_vals)
            print("VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV", employee_vals)
            return request.render('emp.employee_update_success', {})
        else:
            return request.render('emp.access_denied', {})
    
class EmployeePortal(portal.CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id.id
        EmpModel = request.env['emp.model']
        if 'employee_count' in counters:
            if request.env.user.has_group('base.group_portal'):
                values['employee_count'] = EmpModel.search_count([('partner_id','=',partner)]) 
            else:
                values['employee_count'] = EmpModel.search_count([])   
        print("vvvvvvvvvvvvvvvvvvvv", values)     
        return values


    def _get_employee_searchbar_sortings(self):
        return {
            'name': {'label': _('Name A-Z'), 'order': 'name asc'},
            'name1': {'label': _('Name Z-A'), 'order': 'name desc'},
            'employee_code' : {'label': _('Employee Code'), 'order': 'employee_code'},  
            'dob' : {'label': _('Date Of Birth'), 'order': 'dob'},
        }

    def _get_searchbar_inputs(self):
        return {
            'all': {'input': 'all', 'label': _('Search in All')},
            'employee_code.': {'input': 'employee_code', 'label': _('Search in Code')},
            'name': {'input': 'name', 'label': _('Search in Name')},
            'age': {'input': 'age', 'label': _('Search in Age')},
            'states': {'input': 'states', 'label': _('Search in States')},
            'city': {'input': 'city', 'label': _('Search in City')},
        }

    def _get_search_domain(self, search_in, search):
        search_domain = []
        if search_in in ('name', 'all'):
            search_domain = OR([search_domain, [('name', 'ilike', search)]])
        if search_in in ('employee_code', 'all'):
            search_domain = OR([search_domain, [('employee_code', 'ilike', search)]])
        if search_in in ('age', 'all'):
            try:
                age_value = float(search)
                search_domain = OR([search_domain, [('age', '=', age_value)]])
            except ValueError:
                # Handle non-numeric input for age by ignoring it
                pass
        if search_in in ('states', 'all'):
            search_domain = OR([search_domain, [('states', 'ilike', search)]])
        if search_in in ('city', 'all'):
            search_domain = OR([search_domain, [('city', 'ilike', search)]])
        return search_domain
    
    @http.route(['/my/employees', '/my/employees/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_employees(self, page=1, sortby=None, filterby=None,search="",search_in="all", groupby=None ,**kwargs):
        values = self._prepare_portal_layout_values()
        EmpModel = request.env['emp.model']
        partner = request.env.user.partner_id

        url = "/my/employees"

        domain = []
        searchbar_sortings = self._get_employee_searchbar_sortings()

        searchbar_inputs = self._get_searchbar_inputs()
        if not groupby:
            groupby='none'

        groupby_list = {
            'none': {'input': 'none', 'label': _("None"),"order": 1},
            'manager_id': {'input': 'manager_id', 'label': _("Manager"),"order": 1},
            'city': {'input': 'city', 'label': _("City"),"order": 1},
            
        }
        searchbar_filters = {
                'all': {'label': _('All'), 'domain': []},
                'new': {'label': _('New'), 'domain': [('states', '=', 'new')]},
                'probation': {'label': _('Probation'), 'domain': [('states', '=', 'probation')]},
                'employee': {'label': _('Employee'), 'domain': [('states', '=', 'employee')]},
                'notice period': {'label': _('Notice Period'), 'domain': [('states', '=', 'notice period')]},
                'relieved': {'label': _('Relieved'), 'domain': [('states', '=', 'relieved')]},
            }   
        employee_group_by = groupby_list.get(groupby, {})
        if groupby in ('manager_id', 'city'):
            employee_group_by = employee_group_by.get('input')
        else:
            employee_group_by = ''
        # default sort
        if not sortby:
            sortby = 'name'
        order = searchbar_sortings[sortby]['order']

        if not filterby:
            filterby = 'all'

        domain = AND([domain, searchbar_filters[filterby]['domain']])

        if search and search_in:
            domain += self._get_search_domain(search_in, search)

        if request.env.user.has_group('base.group_portal'):
            domain += [('partner_id','=',request.env.user.partner_id.id)]

        # count for pager
        count = EmpModel.search_count(domain)

        # make pager
        pager = portal_pager(
            url='/my/employees',
            url_args={'sortby': sortby, 'filterby': filterby},
            total=count,
            page=page,
            step=7
        )

        employees = EmpModel.sudo().search(domain, order=order, limit=7, offset=pager['offset'])

        if employee_group_by:
            employee_group_list = [{employee_group_by:k, 'employees':EmpModel.concat(*g)} for k, g in groupbyelem(employees, itemgetter(employee_group_by))] 
        else:
            employee_group_list = [{'employees': employees}]

        values.update({
            'employees': employee_group_list,
            'page_name': 'employee',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'groupby': groupby,
            'searchbar_groupby': groupby_list,
            'sortby': sortby,
            'search': search,
            'search_in': search_in,
            'searchbar_inputs': searchbar_inputs,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
            'default_url': "/my/employees",

        })
        return request.render("emp.portal_my_employees", values)
        

    @http.route(['/my/employees/<int:emp_id>'], type='http', auth="public", website=True)
    def portal_employee_page(self, emp_id, report_type=None, access_token=None, message=False, download=False, **kw):
        try:
            employee_sudo = self._document_check_access('emp.model', emp_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        if report_type in ('html', 'pdf','text'):
            return self._show_report(model=employee_sudo, report_type=report_type, report_ref='emp.employee_report_action_new', download=download)

        values = {
            'employee_model': employee_sudo,
            'report_type': 'html',
        }

        values = self._get_page_view_values(
            employee_sudo, access_token, values,False , False)
        return request.render('emp.employee_portal_page_template', values)
