from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from xml.dom.minidom import parseString
import datetime, re, recurly

recurly.SUBDOMAIN = settings.RECURLY_SUBDOMAIN
recurly.API_KEY = settings.RECURLY_API_KEY
recurly.PRIVATE_KEY = settings.RECURLY_PRIVATE_KEY
recurly.DEFAULT_CURRENCY = settings.RECURLY_DEFAULT_CURRENCY


def pretty_print_xml(xml_string):
    line_regex = re.compile(r'\n\n')
    return line_regex.sub('', parseString(xml_string).toprettyxml())

ACCOUNT_STATE_CHOICES = (('active','Active'),('closed','Closed'))
class Account(models.Model):
    user = models.ForeignKey(User)
    account_code = models.CharField(max_length=50)
    state = models.CharField(max_length=10, choices=ACCOUNT_STATE_CHOICES)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=255)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company_name = models.CharField(max_length=50, null=True, blank=True)
    accept_language = models.CharField(max_length=20, null=True, blank=True)
    hosted_login_token = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @classmethod
    def create(cls, user, email, first_name, last_name, company_name=None, accept_language=None, billing_info=None):
        recurly_account = recurly.Account(
            account_code=user.username,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            company_name=company_name,
            accept_language=accept_language,
            billing_info=billing_info
        )
        recurly_account.save()
        
        account = cls(
            user=user, 
            account_code=user.username, 
            username=user.username, 
            email=email, 
            first_name=first_name, 
            last_name=last_name, 
            company_name=company_name, 
            accept_language=accept_language, 
            billing_info=billing_info, 
            created_at=datetime.datetime.now()
        )
        account.save()
        return account
    
    def charge(self, description, unit_amount, quantity, currency, accounting_code=None):
        return Adjustment.create(self.user, self, description, unit_amount, quantity, currency, accounting_code)
    
    def hosted_login_url(self):
        return 'https://{subdomain}.recurly.com/account/{hosted_login_token}'.format(subdomain=settings.RECURLY_SUBDOMAIN, hosted_login_token=self.hosted_login_token)
    
    @property
    def recurly_account(self):
        return recurly.Account.get(self.user.username)
    

class Adjustment(models.Model):
    user = models.ForeignKey(User)
    account = models.ForeignKey(Account)
    uuid = models.CharField(max_length=32, db_indexed=True)
    description = models.CharField(max_length=255)
    accounting_code = models.CharField(max_length=20, null=True, blank=True)
    origin = models.CharField(max_length=20)
    unit_amount = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField()
    discount = models.DecimalField(max_digits=8, decimal_places=2)
    tax = models.DecimalField(max_digits=8, decimal_places=2)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.CharField(max_length=3)
    taxable = models.BooleanField(default=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField()
    invoice = models.ForeignKey('Invoice', null=True, blank=True)
    
    @classmethod
    def create(cls, user, account, description, unit_amount, quantity, currency, accounting_code=None):
        recurly_account = account.recurly_account
        recurly_adjustment = recurly.Adjustment(
            description=description,
            unit_amount_in_cents=int(unit_amount*100),
            currency=currency,
            quantity=quantity,
            accounting_code=accounting_code
        )
        recurly_account.charge(recurly_adjustment)
        
        adjustment = self._create_local(
            user=user, 
            account=account, 
            uuid=recurly_adjustment.uuid, 
            description=description, 
            accounting_code=accounting_code, 
            origin=recurly_adjustment.origin, 
            unit_amount=unit_amount, 
            quantity=quantity, 
            discount=recurly_adjustment.discount_in_cents/100.0,
            tax=recurly_adjustment.tax_in_cents/100.0,
            total=recurly_adjustment.total_in_cents/100.0,
            currency=currency,
            taxable=recurly_adjustment.taxable,
            start_date=recurly_adjustment.start_date,
            end_date=recurly_adjustment.end_date,
            created_at=recurly_adjustment.created_at
        )
        return adjustment
    
    @classmethod
    def _create_local(cls, user, account, description, unit_amount, quantity, currency, accounting_code=None):
        adjustment = cls(
            user=user, 
            account=account, 
            uuid=recurly_adjustment.uuid, 
            description=description, 
            accounting_code=accounting_code, 
            origin=recurly_adjustment.origin, 
            unit_amount=unit_amount, 
            quantity=quantity, 
            discount=recurly_adjustment.discount_in_cents/100.0,
            tax=recurly_adjustment.tax_in_cents/100.0,
            total=recurly_adjustment.total_in_cents/100.0,
            currency=currency,
            taxable=recurly_adjustment.taxable,
            start_date=recurly_adjustment.start_date,
            end_date=recurly_adjustment.end_date,
            created_at=recurly_adjustment.created_at
        )
        adjustment.save()
        return adjustment

class BillingInfo(models.Model):
    user = models.ForeignKey(User)
    account = models.ForeignKey(Account)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company = models.CharField(max_length=50, null=True, blank=True)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=20)
    zipcode = models.CharField(max_length=10)
    country = models.CharField(max_length=2)
    phone = models.CharField(max_length=15)
    vat_number = models.CharField(max_length=20, null=True, blank=True)
    ip_address = models.CharField(max_length=20)
    ip_address_country = models.CharField(max_length=2)
    card_type = models.CharField(max_length=10)
    year = models.IntegerField()
    month = models.IntegerField()
    first_six = models.CharField(max_length=6, null=True, blank=True)
    last_four = models.CharField(max_length=4, null=True, blank=True)
    paypal_billing_agreement_id = models.CharField(max_length=20, null=True, blank=True)
    
    @classmethod
    def create(cls, account, first_name, last_name, company, address1, address2, city, state, zipcode, country, phone, vat_number, ip_address, ip_address_country, number, verification_value, month, year):
        recurly_account = account.recurly_account
        recurly_billing_info = recurly_account.billing_info
        recurly_billing_info.first_name = first_name
        recurly_billing_info.last_name = last_name
        recurly_billing_info.company = company
        recurly_billing_info.address1 = address1
        recurly_billing_info.address2 = address2
        recurly_billing_info.city = city
        recurly_billing_info.state = state
        recurly_billing_info.zip = zipcode
        recurly_billing_info.country = country
        recurly_billing_info.phone = phone
        recurly_billing_info.vat_number = vat_number
        recurly_billing_info.ip_address = ip_address
        recurly_billing_info.ip_address_country = ip_address_country
        recurly_billing_info.number = number
        recurly_billing_info.verification_value = verification_value
        recurly_billing_info.month = month
        recurly_billing_info.year = year
        recurly_billing_info.save()
        
        billing_info = cls(
            user = account.user,
            account = account,
            first_name = first_name,
            last_name = last_name,
            company = company,
            address1 = address1,
            address2 = address2,
            city = city,
            state = state,
            zipcode = zipcode,
            country = country,
            phone = phone,
            vat_number = vat_number,
            ip_address = ip_address,
            ip_address_country = ip_address_country,
            card_type = recurly_billing_info.card_type,
            year = year,
            month = month,
            first_six = recurly_billing_info.first_six,
            last_four = recurly_billing_info.last_four
        )
        billing_info.save()
        return billing_info

class Coupon(models.Model):
    coupon_code = models.CharField(max_length=50, db_index=True)
    name = models.CharField(max_length=50)
    state = models.CharField(max_length=20)
    hosted_description = models.CharField(max_length=255)
    invoice_description = models.CharField(max_length=255)
    discount_type = models.CharField(max_length=15)
    discount_percent = models.IntegerField(null=True, blank=True)
    discount_dollars = models.DecimalField(max_digits=8, decimal_places=2)
    redeem_by_date = models.DateTimeField(null=True, blank=True)
    single_use = models.BooleanField(default=False)
    applies_for_months = models.IntegerField(null=True, blank=True)
    max_redemptions = models.IntegerField(null=True, blank=True)
    applies_to_all_plans = models.BooleanField(default=True)
    created_at = models.DateTimeField()
    plans = models.ManyToManyField('Plan')
    
    @classmethod
    def create(cls, coupon_code, name, hosted_description, invoice_description, redeem_by_date, single_use, applies_for_months, max_redemptions, applies_to_all_plans, discount_type, discount_percent, discount_dollars, plan_codes=[]):
        recurly_coupon = recurly.Coupon(
            coupon_code=coupon_code,
            name=name,
            hosted_description=hosted_description,
            invoice_description=invoice_description,
            redeem_by_date=redeem_by_date,
            single_use=single_use,
            applies_for_month=applies_for_months,
            max_redemptions=max_redemptions,
            applies_to_all_plans=applies_to_all_plans,
            discount_type=discount_type,
            plan_codes=plan_codes
        )
        
        if discount_type == 'percent':
            recurly_coupon.discount_percent=discount_percent
        elif discount_type == 'dollars':
            recurly_coupon.discount_in_cents=int(discount_dollars*100)
            
        recurly_coupon.save()
        
        coupon = cls(
            coupon_code = coupon_code,
            name = name,
            state = recurly_coupon.state,
            discount_type = discount_type,
            discount_percent = discount_percent,
            discount_dollars = discount_dollars,
            redeem_by_date = redeem_by_date,
            single_use = single_use,
            applies_for_months = applies_for_months,
            max_redemptions = max_redemptions,
            applies_to_all_plans = applies_to_all_plans,
            created_at = recurly_coupon.created_at,
            plans = Plan.objects.filter(plan_code__in=plan_codes)
        )
        coupon.save()
        return coupon
    
    @property
    def recurly_coupon(self):
        return recurly.Coupon.get(self.coupon_code)

class CouponRedemption(models.Model):
    coupon = models.ForeignKey(Coupon)
    account = models.ForeignKey(Account)
    user = models.ForeignKey(User)
    single_use = models.BooleanField(default=False)
    total_discounted = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.CharField(max_length=3)
    state = models.CharField(max_length=20)
    created_at = models.DateTimeField()
    
    @classmethod
    def create(cls, coupon, account, currency):
        recurly_coupon = coupon.recurly_coupon
        
        recurly_coupon_redemption = recurly.Redemption(
            account_code = account.account_code,
            currency = currency
        )
        recurly_coupon_redemption.save()
        
        coupon_redemption = cls(
            coupon = coupon,
            account = account,
            user = account.user,
            single_use = recurly_coupon_redemption.single_use,
            total_discounted = recurly_coupon_redemption.total_discounted_in_cents / 100.0,
            currency = currency,
            state = recurly_coupon_redemption.state,
            created_at = recurly_coupon_redemption.created_at
        )
        coupon_redemption.save()
        return coupon_redemption

class Invoice(models.Model):
    account = models.ForeignKey(Account)
    user = models.ForeignKey(User)
    uuid = models.CharField(max_length=32, db_indexed=True)
    state = models.CharField(max_length=20)
    invoice_number = models.IntegerField()
    po_number = models.CharField(max_length=20, null=True, blank=True)
    vat_number = models.CharField(max_length=20, null=True, blank=True)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)
    tax = models.DecimalField(max_digits=8, decimal_places=2)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.CharField(max_length=3)
    created_at = models.DateTimeField()
    
    @classmethod
    def create(cls, account):
        recurly_account = account.recurly_account
        recurly_invoice = recurly_account.invoice()
        
        invoice = cls(
            account = account,
            user = account.user,
            uuid = recurly_invoice.uuid,
            state = recurly_invoice.state,
            invoice_number = recurly_invoice.invoice_number,
            po_number = recurly_invoice.po_number,
            vat_number = recurly_invoice.vat_number,
            subtotal = recurly_invoice.subtotal_in_cents / 100.0,
            tax = recurly_invoice.tax_in_cents / 100.0,
            total = recurly_invoice.total_in_cents / 100.0,
            currency = recurly_invoice.currency,
            created_at = recurly_invoice.created_at
        )
        invoice.save()
         
        for line_item in recurly_invoice.line_items:
            try:
                adjustment = account.adjustment_set.get(uuid=line_item.uuid)
            except DoesNotExist as dne:
                adjustment = Adjustment._create_local(account.user, account, line_item.description, line_item.unit_amount, line_item.quantity, line_item.currency, line_item.accounting_code)
            
            adjustment.invoice = self
            adjustment.save()
        
        for recurly_transaction in recurly_invoice.transactions:
            try:
                transaction = account.transaction_set.get(uuid=recurly_transaction.uuid)
            except DoesNotExist as dne:
                pass #TODO: Transaction._create_local
            
            transaction.invoice = self
            transaction.save()
            
        return invoice
            
PLAN_UNIT_CHOICES = (('days', 'Days'), ('months', 'Months'))
class Plan(models.Model):
    plan_code = models.CharField(max_length=50, db_indexed=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    success_url = models.URLField(max_length=255, null=True, blank=True)
    cancel_url = models.URLField(max_length=255, null=True, blank=True)
    display_donation_amounts = models.BooleanField(default=False)
    display_quantity = models.BooleanField(default=False)
    display_phone_number = models.BooleanField(default=False)
    bypass_hosted_confirmation = models.BooleanField(default=False)
    unit_name = models.CharField(max_length=20, default='users')
    payment_page_tos_link = models.URLField(max_length=255, null=True, blank=True)
    plan_interval_length = models.IntegerField(default=1)
    plan_interval_unit = models.CharField(max_length=20, choices=PLAN_UNIT_CHOICES, default='months')
    trial_interval_length = models.IntegerField(default=0)
    trial_interval_unit = models.CharField(max_length=20, choices=PLAN_UNIT_CHOICES, default='months')
    accounting_code = models.CharField(max_length=20, null=True, blank=True) 
    created_at = models.DateTimeField()
    unit_amount = models.DecimalField(max_digits=8, decimal_places=2)
    setup_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    
    @classmethod
    def create(cls, plan_code, name, description, accounting_code, plan_interval_unit, plan_interval_length, trial_interval_unit, trial_interval_length, setup_fee, unit_amount, total_billing_cycles, unit_name, display_quantity, success_url, cancel_url):
        recurly_plan = recurly.Plan(
            plan_code = plan_code,
            name = name,
            description = description,
            accounting_code = accounting_code,
            plan_interval_unit = plan_interval_unit,
            plan_interval_length = plan_interval_length,
            trial_interval_unit = trial_interval_unit,
            trial_interval_length = trial_interval_length,
            setup_fee_in_cents = recurly.resource.Money(int(setup_fee * 100)),
            unit_amount_in_cents = recurly.resource.Money(int(unit_amount * 100)),
            total_billing_cycles = total_billing_cycles,
            unit_name = unit_name,
            display_quantity = display_quantity,
            success_url = success_url,
            cancel_url = cancel_url
        )
        recurly_plan.save()
        
        plan = cls(
            plan_code = plan_code,
            name = name,
            description = description,
            accounting_code = accounting_code,
            plan_interval_unit = plan_interval_unit,
            plan_interval_length = plan_interval_length,
            trial_interval_unit = trial_interval_unit,
            trial_interval_length = trial_interval_length,
            setup_fee_in_cents = setup_fee,
            unit_amount_in_cents = unit_amount,
            total_billing_cycles = total_billing_cycles,
            unit_name = unit_name,
            display_quantity = display_quantity,
            success_url = success_url,
            cancel_url = cancel_url,
            display_donation_amounts = recurly_plan.display_donation_amounts,
            display_phone_number = recurly_plan.display_phone_number,
            bypass_hosted_confirmation = recurly_plan.bypass_hosted_confirmation,
            payment_page_tos_link = recurly_plan.payment_page_tos_link,
            created_at = recurly_plan.payment_page_tos_link
        )
        plan.save()
        return plan

class PlanAddOn(models.Model):
    pass

class Subscription(models.Model):
    pass

class Transaction(models.Model):
    pass



class OrderTransaction(models.Model):

    # Note we don't use a foreign key as the order hasn't been created
    # by the time the transaction takes place
    order_number = models.CharField(max_length=128, db_index=True, null=True)

    # Transaction type
    txn_type = models.CharField(max_length=12)
    txn_ref = models.CharField(max_length=16)
    amount = models.DecimalField(decimal_places=2,
                                 max_digits=12,
                                 blank=True,
                                 null=True
                                 )

    response_code = models.CharField(max_length=2)
    response_message = models.CharField(max_length=255)

    # For debugging purposes
    request_xml = models.TextField()
    response_xml = models.TextField()

    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_created',)

    def save(self, *args, **kwargs):
        if not self.pk:
            cc_regex = re.compile(r'\d{12}')
            self.request_xml = cc_regex.sub('XXXXXXXXXXXX', self.request_xml)
            ccv_regex = re.compile(r'<Cvc2>\d+</Cvc2>')

            self.request_xml = ccv_regex.sub('<Cvc2>XXX</Cvc2>',
                                             self.request_xml)

            pw_regex = re.compile(r'<PostPassword>.*</PostPassword>')
            self.request_xml = pw_regex.sub('<PostPassword>XXX</PostPassword>',
                                            self.request_xml)

        super(OrderTransaction, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s txn for order %s - ref: %s, message: %s' % (
            self.txn_type,
            self.order_number,
            self.txn_ref,
            self.response_message,
        )

    @property
    def pretty_request_xml(self):
        return pretty_print_xml(self.request_xml)

    @property
    def pretty_response_xml(self):
        return pretty_print_xml(self.response_xml)
