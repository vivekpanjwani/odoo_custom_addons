from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
from lxml import etree
from datetime import date


class EmpModel(models.Model):
    _inherit = ['portal.mixin','mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _name = 'emp.model'
    _description = 'Employee Information'


    name = fields.Char(
        string="Employee Name",
        required=True)
    
    date_time=fields.Datetime(
        string="Date Time",
        default=fields.Datetime.now)

    tag_ids = fields.Many2many(
        'emp.tag', 'employee_tag_rel',
        'emp_id', 'tag_id',
        string='Tags')

    color = fields.Integer(string="Color Index", default=0)

    image = fields.Image()
    dob = fields.Date(string="Date of Birth")
    age = fields.Float(string="Age", compute="_compute_age", store=True)
    _sql_constraints = [
        ('dob_not_in_future', 'CHECK (dob <= CURRENT_DATE)',
         'Date of Birth must be today\'s date or earlier.'),
    ]
    gender = fields.Selection([('Male','Male'),('Female','Female'),("Others", "Others")])
    blood_group = fields.Selection([('A+', 'A+'),('A-', 'A-'),('B+', 'B+'),('AB+', 'AB+'),('O+', 'O+'),('O-', 'O-'),('B-', 'B-'),('AB-', 'AB-'),])

    # active = fields.Boolean(default=True)
    phone = fields.Char(string="Phone")
    partner_id = fields.Many2one('res.partner')
    partner_id_readonly = fields.Boolean(compute='_compute_partner_id_readonly')
    basic_salary = fields.Float(string='Basic Salary')

    street = fields.Char(string="Street")
    street2 = fields.Char(string="Street2")
    city = fields.Many2one('city.city',string="City")
    zip = fields.Char(string="Zip")
    state_id = fields.Many2one('res.country.state', string="State")
    country_id = fields.Many2one('res.country', string="Country")
    email = fields.Char(string='Email')
    marital_status = fields.Selection([('Married', 'Married'), ('Unmarried', 'Unmarried'), ('Divorced', 'Divorced')], string = 'Maritial Status')
    marriage_date = fields.Date(string="Marriage Date")
    signature = fields.Html(string="Signature")
    document_id = fields.One2many('emp.documents','employee_id', string="Documents")

    employee_code = fields.Char(string="Employee Code", readonly=1)
    designation_id = fields.Many2one('designation.designation',string = "Designtaion", )
    currency_id = fields.Many2one('res.currency', string="Currency")
    company_id = fields.Many2one('res.company',related="designation_id.company", string="Company")
    salary_id = fields.Monetary(related="designation_id.salary" ,string="Salary", readonly=True, currency_field="currency_id")

    emp_contract=fields.Many2many(
        comodel_name='emp.contract',
        relation='emp_cont_id',
        string="Contract")

    date = fields.Date(string='Date')
    
    date_start = fields.Date(string='Start Date')
    date_stop = fields.Date(string='End Date')
    interval = fields.Selection([
        ('day', 'Day'),
        ('week', 'Week'),
        ('month', 'Month'),
        ('year', 'Year'),
    ], string='Interval', default='month')
     
    prohibation_period = fields.Integer(string="Prohibation Period")
    notice_period = fields.Integer(string="Notice Period")

    states = fields.Selection(
        [
            ('new', 'New'),
            ('probation', 'Probation'),
            ('employee', 'Employee'),
            ('notice period', 'Notice Period'),
            ('relieved', 'Relieved'),
        ],
        string="States",
        readonly=True, copy=False, index=True,
        tracking=3,
        default='new',
    )

    released_date = fields.Date(string="Released Date")

    joining_date = fields.Date(string="Joining Date")
    joined = fields.Boolean(string='Joined', default=False)

    is_manager=fields.Boolean(string="IsManager")
    manager_id = fields.Many2one('res.users', string="Manager")
    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")
    net_salary = fields.Float(string="Net Salary")
    gross_salary = fields.Float(string="Gross Salary")
    commision = fields.Integer(string="Commision")
    extra_allowances=fields.Float(string="Extra Allowances")
    payslip_bill_count = fields.Integer(compute='_compute_payslip_bill_count')

    employee_count = fields.Integer("Employee Count", compute="_employee_count")
    
    @api.depends('name')
    def _employee_count(self):
        count=self.env['emp.model'].search_count([])
        print("CCCCCCCCCCCCCCCCCCC", count)

        self.employee_count=count

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
            if self.partner_id:
                self.name = self.partner_id.name
                
    @api.onchange('country_id')
    def _onchange_country_id(self):
        if self.country_id and self.state_id.country_id != self.country_id:
            self.state_id = False

    @api.onchange('state_id')
    def _onchange_state_id(self):
        if self.state_id:
            self.country_id = self.state_id.country_id

    @api.onchange('city')
    def _onchange_city(self):
        if self.city:
            self.state_id = self.city.state_ids

    @api.onchange('phone')
    def _onchange_phone(self):
        for record in self:
            mobile = record.phone
            if mobile:
                if mobile.startswith('91') and len(mobile) == 12:
                    record.phone = "+" + mobile
                elif not mobile.startswith('91') and len(mobile) == 10:
                    record.phone = "+91" + mobile
                elif mobile.startswith("91") and len(mobile) == 10:
                    record.phone = "+91" + mobile
                elif mobile.startswith('9191') and len(mobile) == 12:
                    record.phone = '+' + mobile
                else:
                    return None
                    # raise ValidationError(_("Invalid phone number format."))

    def _compute_partner_id_readonly(self):
        for record in self:
            record.partner_id_readonly = bool(record.id)
    
    @api.onchange('released_date')
    def _onchange_released_date(self):
        if not self.released_date:
            self.states = 'new'

    def set_notice_period(self):
        self.states = 'notice period'

    def set_cancel(self):
        self.states = 'new'

    def set_probation(self):
        if self.joining_date and self.states != 'probation':
            self.states = 'probation'
            self.joined = True
        elif not self.joining_date:
            self.states = "new"

    def update_state(self):
        probation_period_in_days = self.env['ir.config_parameter'].sudo().get_param('probation_period_in_days')
        probation_period_in_days = int(probation_period_in_days)
        today = fields.Date.today()
        # probation_date = today - timedelta(days=probation_period_in_days)
        records = self.search([('states', '=', 'probation')])
        for rec in records:
            rec.states = 'employee'

    def update_state2(self):
        notice_period_in_days = self.env['ir.config_parameter'].sudo().get_param('notice_period_in_days')
        notice_period_in_days = int(notice_period_in_days)
        today = fields.Date.today()
        records = self.search([('states', '=', 'notice period'), ('released_date', '!=', False)])
        for rec in records:
            # if rec.released_date and (today - rec.released_date).days >= notice_period_in_days:
            rec.states = 'relieved'

    def name_get(self):
            result = []
            for record in self:
                name = f"[{record.employee_code}] - {record.name}"
                result.append((record.id, name))
            return result

    @api.depends('dob')
    def _compute_age(self):
        today = date.today()
        for emp in self:
            if emp.dob:
                dob = fields.Date.from_string(emp.dob)
                emp.age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                if emp.age < 18:
                    raise ValidationError('Age must be more than 18')
            else:
                emp.age = 0


    @api.onchange('gender')
    def _onchange_gender(self):
        if self.gender == 'Others':
            return {
                    'warning': {'title': "Warning", 'message': "What is this?", 'type': 'notification'},
                }

    def update_related_contacts(self):
        for record in self:
            # Update related contacts
            contacts = self.env['res.partner'].search([('id', '=', record.partner_id.id)])
            for contact in contacts:
                contact.name = record.name
                contact.country_id = record.country_id.id
                contact.state_id = record.state_id.id
                contact.city = record.city.name if record.city else False
                contact.street = record.street
                contact.street2 = record.street2

    @api.model_create_multi
    def create(self, vals_list):
        print("#################################### ")
        
        for vals in vals_list:
            existing_record = self.search([('name', '=', vals.get('name'))], limit=1)
            if existing_record:
                # Create a duplicate record
                vals['name'] = "{} (copy)".format(vals['name'])
                duplicate_record = self.create(vals)
                return duplicate_record
            
            # Create a new partner
            partner = self.env['res.partner'].create({
                'name': vals.get('name'),
                'street': vals.get('street'),
                'street2': vals.get('street2'),
                'state_id': vals.get('state_id'),
                'country_id': vals.get('country_id'),
                'city': vals.get('city'),
            })
            user_vals = {
                'name': vals.get('name'),
                'login': 'login@gmail.com',
                # 'groups_id': [(4, self.env.ref('base.group_user').id), (4, self.env.ref('base.group_emp_manager_custom').id)],
            }
            user_id = self.env['res.users'].create(user_vals)
            vals['partner_id'] = partner.id

            if 'company_id' in vals:
                self = self.with_company(vals['company_id'])
            if vals.get('employee_code', _("New")) == _("New"):
                seq_date = fields.Datetime.context_timestamp(
                    self, fields.Datetime.to_datetime(vals['date_time'])
                ) if 'date_time' in vals else None
                vals['employee_code'] = self.env['ir.sequence'].next_by_code(
                    'emp.model', sequence_date=seq_date) or _("New")
                
                
            if self.search([('employee_code', '=', vals.get('employee_code'))]):
                vals['employee_code'] = self.env['ir.sequence'].next_by_code('emp.model')
            
   
        # return super().create(vals_list)
        res = super().create(vals_list)
        print(res)
        for record in res:
            self.env['emp.personal.info'].create({'emp_id': record.id})
        
        for record in res:
            record.update_related_contacts()
        return res

    def write(self,vals):
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        res = super().write(vals)

        if 'partner_id' in vals:
            for record in self:
                partner = record.partner_id
                partner.name = record.name

        self.update_related_contacts()
        return super().write(vals)
    
    def unlink(self):
        partners_to_delete = self.mapped('partner_id')
        res = super().unlink()
        partners_to_delete.unlink()
        return res
    
    def button_send_assessment_email(self):
        self.ensure_one()
        if self.states == 'employee':
            template = self.env.ref('emp.email_template_edi_emp_custom')
            template.send_mail(self.id)

    @api.depends('partner_id')
    def _compute_payslip_bill_count(self):
        for record in self:
            record.payslip_bill_count = self.env['account.move'].search_count([
                ('partner_id', '=', record.partner_id.id),
                ('move_type', '=', 'in_invoice'),
            ])

    def payment_action(self):

        return {
            'type': 'ir.actions.act_window',
            'name': 'Payslip Bills',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('partner_id', '=', self.partner_id.id), ('move_type', '=', 'in_invoice')],
        }
        
    def action_preview_employee(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': self.get_portal_url(),
        }


    def _get_portal_return_action(self):
        """ Return the action used to display orders when returning from customer portal. """
        self.ensure_one()
        return self.env.ref('emp.action_emp_model')

    # portal.mixin override
    def _compute_access_url(self):
        super()._compute_access_url()
        for order in self:
            order.access_url = f'/my/employees/{order.id}'
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",order.access_url )
        if not self.env['emp.model'].check_access_rights('create', False):
            try:
                self.check_access_rights('write')
                self.check_access_rule('write')
                print('####################################')
            except AccessError:
                print("ERERERERERERERERERERERERERERERE")
                return self.env['emp.model']

