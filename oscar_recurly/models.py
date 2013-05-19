from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from xml.dom.minidom import parseString
import datetime, re, recurly

recurly.SUBDOMAIN = settings.RECURLY_SUBDOMAIN
recurly.API_KEY = settings.RECURLY_API_KEY
recurly.PRIVATE_KEY = settings.RECURLY_PRIVATE_KEY
recurly.DEFAULT_CURRENCY = settings.RECURLY_DEFAULT_CURRENCY


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
    
    class Meta:
        ordering = ('-pk')
    
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
    
    class Meta:
        ordering = ('-pk')
    
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
    def _create_local(cls, user, account, uuid, description, accounting_code, origin, unit_amount, quantity, discount, tax, total, currency, taxable, start_date, end_date, created_at):
        adjustment = cls(
            user=user, 
            account=account, 
            uuid=uuid, 
            description=description, 
            accounting_code=accounting_code, 
            origin=origin, 
            unit_amount=unit_amount, 
            quantity=quantity, 
            discount=discount,
            tax=tax,
            total=total,
            currency=currency,
            taxable=taxable,
            start_date=start_date,
            end_date=end_date,
            created_at=created_at
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
    
    class Meta:
        ordering = ('-pk')
    
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
    
    class Meta:
        ordering = ('coupon_code',)
    
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
    
    class Meta:
        ordering = ('-pk')
    
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
    
    class Meta:
        ordering = ('-pk')
    
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
                adjustment = Adjustment._create_local(account.user, account, line_item.uuid, line_item.description, line_item.accounting_code, line_item.origin, line_item.unit_amount_in_cents / 100.0, line_item.quantity, line_item.discount_in_cents / 100.0, line_item.tax_in_cents / 100.0 , line_item.total_in_cents / 100.0, line_item.currency, line_item.taxable, line_item.start_date, line_item.end_date, line_item.created_at)
            
            adjustment.invoice = self
            adjustment.save()
        
        for recurly_transaction in recurly_invoice.transactions:
            try:
                transaction = account.transaction_set.get(uuid=recurly_transaction.uuid)
            except DoesNotExist as dne:
                transaction = Transaction._create_local(account, account.user, recurly_transaction.invoice, recurly_transaction.subscription, recurly_transaction.uuid, recurly_transaction.action, recurly_transaction.amount_in_cents / 100.0, 
                    recurly_transaction.tax_in_cents / 100.0, recurly_transaction.currency, recurly_transaction.status, recurly_transaction.source, recurly_transaction.reference, recurly_transaction.test, 
                    recurly_transaction.voidable, recurly_transaction.refundable, recurly_transaction.cvv_result, recurly_transaction.avs_result, recurly_transaction.avs_result_street, 
                    recurly_transaction.avs_result_postal, recurly_transaction.created_at, recurly_transaction.account.account_code, recurly_transaction.account.first_name, recurly_transaction.account.last_name, 
                    recurly_transaction.account.company, recurly_transaction.account.billing_info.first_name, recurly_transaction.account.billing_info.last_name, recurly_transaction.account.billing_info.address1, 
                    recurly_transaction.account.billing_info.address2, recurly_transaction.account.billing_info.city, recurly_transaction.account.billing_info.state, recurly_transaction.account.billing_info.zip, 
                    recurly_transaction.account.billing_info.country, recurly_transaction.account.billing_info.phone, recurly_transaction.account.billing_info.vat_number, 
                    recurly_transaction.account.billing_info.card_type, recurly_transaction.account.billing_info.year, recurly_transaction.account.billing_info.month, recurly_transaction.account.billing_info.first_six,
                    recurly_transaction.account.billing_info.last_four)
            
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
    
    class Meta:
        ordering = ('plan_code',)
    
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
    
    @property
    def recurly_plan(self):
        return recurly.Plan.get(self.plan_code)

class PlanAddOn(models.Model):
    plan = models.ForeignKey(Plan)
    add_on_code = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    display_quantity_on_hosted_page = models.BooleanField(default=True)
    default_quantity = models.IntegerField(default=1)
    unit_amount = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField()
    
    class Meta:
        ordering = ('plan', 'add_on_code',)
    
    @classmethod
    def create(cls, plan, add_on_code, name, unit_amount, default_quantity, display_quantity_on_hosted_page, accounting_code):
        recurly_plan = plan.recurly_plan
        recurly_plan_add_on = recurly.AddOn(
            add_on_code = add_on_code,
            name = name,
            unit_amount_in_cents = recurly.resource.Money(int(unit_amount * 100)),
            default_quantity = default_quantity,
            display_quantity_on_hosted_page = display_quantity_on_hosted_page,
            accounting_code = accounting_code
        )
        recurly_plan.create_add_on(recurly_plan_add_on)
        
        plan_add_on = cls(
            plan = plan,
            add_on_code = add_on_code,
            name = name,
            unit_amount = unit_amount,
            default_quantity = default_quantity,
            display_quantity_on_hosted_page = display_quantity_on_hosted_page,
            accounting_code = accounting_code,
            created_at = recurly_plan_add_on.created_at
        )
        plan_add_on.save()
        return plan_add_on
        

class Subscription(models.Model):
    account = models.ForeignKey(Account)
    user = models.ForeignKey(User)
    plan = models.ForeignKey(Plan)
    uuid = models.CharField(max_length=32, db_indexed=True)
    state = models.CharField(max_length=20)
    unit_amount = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.CharField(max_length=3)
    quantity = models.IntegerField(default=1)
    activated_at = models.DateTimeField()
    canceled_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField()
    current_period_started_at = models.DateTimeField()
    current_period_ends_at = models.DateTimeField()
    trial_started_at = models.DateTimeField(null=True, blank=True)
    trial_ends_at = models.DateTimeField(null=True, blank=True)
    subscription_add_ons = models.ManyToManyField(PlanAddOn, null=True, blank=True)
    
    class Meta:
        ordering = ('-pk')
    
    @classmethod
    def create(cls, plan, account, subscription_add_ons, coupon_code, unit_amount, currency, quantity, trial_ends_at, starts_at, total_billing_cycles, first_renewal_date):
        recurly_account = account.recurly_account
        recurly_subscription = recurly.Subscription(
            plan_code = plan.plan_code,
            account = recurly_account,
            coupon_code = coupon_code,
            unit_amount_in_cents = recurly.resource.Money(int(unit_amount * 100)),
            currency = currency,
            quantity = quantity,
            trial_ends_at = trial_ends_at,
            starts_at = starts_at,
            total_billing_cycles = total_billing_cycles,
            first_renewal_date = first_renewal_date
        )
        
        if subscription_add_ons:
            #TODO Add-ons
            pass
        recurly_subscription.save()
        
        subscription = cls(
            account = account,
            user = account.user,
            plan = plan,
            uuid = recurly_subscription.uuid,
            state = recurly_subscription.state,
            unit_amount = unit_amount,
            currency = currency,
            quantity = quantity,
            activated_at = recurly_subscription.activated_at,
            canceled_at = recurly_subscription.canceled_at,
            expires_at = recurly_subscription.expires_at,
            current_period_started_at = recurly_subscription.current_period_started_at,
            current_period_ends_at = recurly_subscription.current_period_ends_at,
            trial_started_at = recurly_subscription.trial_started_at,
            trial_ends_at = trial_ends_at
        )
        subscription.save()
        return subscription

TRANSACTION_ACTION_CHOICES = (
    ('purchase', 'Purchase'), 
    ('authorization', 'Authorization'), 
    ('refund', 'Refund'),
)
TRANSACTION_SOURCE_CHOICES = (
    ('transaction', 'One-time Transaction'),
    ('subscription', 'Subscription'),
    ('billing_info', 'Updated Billing Info'),
)
TRANSACTION_STATUS_CHOICES = (
    ('success', 'Success'),
    ('failed', 'Failed'),
    ('void', 'Void'),
)
class Transaction(models.Model):
    account = models.ForeignKey(Account)
    user = models.ForeignKey(User)
    invoice = models.ForeignKey(Invoice, null=True, blank=True)
    subscription = models.ForeignKey(Subscription, null=True, blank=True)
    uuid = models.CharField(max_length=32)
    action = models.CharField(max_length=20, choices=TRANSACTION_ACTION_CHOICES)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    tax = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.CharField(max_length=3)
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUS_CHOICES)
    source = models.CharField(max_length=20, choices=TRANSACTION_SOURCE_CHOICES)
    reference = models.CharField(max_length=50)
    test = models.BooleanField()
    voidable = models.BooleanField()
    refundable = models.BooleanField()
    cvv_result = models.CharField(max_length=50)
    avs_result = models.CharField(max_length=50)
    avs_result_street = models.CharField(max_length=50)
    avs_result_postal = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    account_account_code = models.CharField(max_length=50)
    account_first_name = models.CharField(max_length=50)
    account_last_name = models.CharField(max_length=50)
    account_company = models.CharField(max_length=50, null=True, blank=True)
    billing_info_first_name = models.CharField(max_length=50)
    billing_info_last_name = models.CharField(max_length=50)
    billing_info_address1 = models.CharField(max_length=100)
    billing_info_address2 = models.CharField(max_length=100, null=True, blank=True)
    billing_info_city = models.CharField(max_length=100)
    billing_info_state = models.CharField(max_length=20)
    billing_info_zip = models.CharField(max_length=10)
    billing_info_country = models.CharField(max_length=2)
    billing_info_phone = models.CharField(max_length=15)
    billing_info_vat_number = models.CharField(max_length=20, null=True, blank=True)
    billing_info_card_type = models.CharField(max_length=10)
    billing_info_year = models.IntegerField()
    billing_info_month = models.IntegerField()
    billing_info_first_six = models.CharField(max_length=6)
    billing_info_last_four = models.CharField(max_length=4)
    
    class Meta:
        ordering = ('-pk')
    
    @classmethod
    def create(cls, account, amount, currency, description):
        recurly_account = account.recurly_account
        recurly_transaction = recurly.Transaction(
            account = recurly_account,
            amount_in_cents = int(amount * 100),
            currency = currency,
            description = description
        )
        recurly_transaction.save()
        
        transaction = self._create_local(account, account.user, recurly_transaction.invoice, recurly_transaction.subscription, recurly_transaction.uuid, recurly_transaction.action, recurly_transaction.amount_in_cents / 100.0, 
            recurly_transaction.tax_in_cents / 100.0, recurly_transaction.currency, recurly_transaction.status, recurly_transaction.source, recurly_transaction.reference, recurly_transaction.test, 
            recurly_transaction.voidable, recurly_transaction.refundable, recurly_transaction.cvv_result, recurly_transaction.avs_result, recurly_transaction.avs_result_street, 
            recurly_transaction.avs_result_postal, recurly_transaction.created_at, recurly_transaction.account.account_code, recurly_transaction.account.first_name, recurly_transaction.account.last_name, 
            recurly_transaction.account.company, recurly_transaction.account.billing_info.first_name, recurly_transaction.account.billing_info.last_name, recurly_transaction.account.billing_info.address1, 
            recurly_transaction.account.billing_info.address2, recurly_transaction.account.billing_info.city, recurly_transaction.account.billing_info.state, recurly_transaction.account.billing_info.zip, 
            recurly_transaction.account.billing_info.country, recurly_transaction.account.billing_info.phone, recurly_transaction.account.billing_info.vat_number, 
            recurly_transaction.account.billing_info.card_type, recurly_transaction.account.billing_info.year, recurly_transaction.account.billing_info.month, recurly_transaction.account.billing_info.first_six,
            recurly_transaction.account.billing_info.last_four)
        return transaction
        
    @classmethod
    def _create_local(cls, account, user, invoice, subscription, uuid, action, amount, tax, currency, status, source, reference, test, voidable, refundable, cvv_result, avs_result, avs_result_street, avs_result_postal, 
                        created_at, account_account_code, account_first_name, account_last_name, account_company, billing_info_first_name, billing_info_last_name, billing_info_address1, billing_info_address2, 
                        billing_info_city, billing_info_state, billing_info_zip, billing_info_country, billing_info_phone, billing_info_vat_number, billing_info_card_type, billing_info_year, billing_info_month, 
                        billing_info_first_six, billing_info_last_four):
        transaction = cls(
            account = account, 
            user = user, 
            invoice = invoice, 
            subscription = subscription, 
            uuid = uuid, 
            action = action, 
            amount = amount, 
            tax = tax, 
            currency = currency, 
            status = status,
            source = source, 
            reference = reference, 
            test = test,
            voidable = voidable,
            refundable = refundable,
            cvv_result = cvv_result,
            avs_result = avs_result,
            avs_result_street = avs_result_street,
            avs_result_postal = avs_result_postal,
            created_at = created_at,
            account_account_code = account_account_code,
            account_first_name = account_first_name,
            account_last_name = account_last_name,
            account_company = account_company,
            billing_info_first_name = billing_info_first_name,
            billing_info_last_name = billing_info_last_name,
            billing_info_address1 = billing_info_address1,
            billing_info_address2 = billing_info_address2,
            billing_info_city = billing_info_city,
            billing_info_state = billing_info_state,
            billing_info_zip = billing_info_zip,
            billing_info_country = billing_info_country,
            billing_info_phone = billing_info_phone,
            billing_info_vat_number = billing_info_vat_number,
            billing_info_card_type = billing_info_card_type,
            billing_info_year = billing_info_year,
            billing_info_month = billing_info_month,
            billing_info_first_six = billing_info_first_six,
            billing_info_last_four = billing_info_last_four,
        )
        transaction.save()
        return transaction
