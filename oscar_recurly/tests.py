from django.contrib.auth.models import User
from django.test import TestCase

from oscar.apps.customer.forms import EmailUserCreationForm
from oscar_recurly.models import *

from .utils import *

import decimal, logging, random

logger = logging.getLogger(__file__)

class TestCase(TestCase):
    account = None
    user = None
    billing_info = None
    plan = None
    subscription = None
    
    def test_recurly_functionality(self):
        random.seed()
        
        # create random user registration.
        email = address_generator().next()
        first_name = gen_name(7)
        last_name = gen_name(8)
        password = 'oscar_recurly'

        registration_form_data = {
            'email': email,
            'password1': password,
            'password2': password
        }
        
        percent_off_coupon_code = percent_off_coupon_name = gen_name(15)
        percent_off = random.randrange(100)
        
        dollar_off_coupon_code = dollar_off_coupon_name = gen_name(15)
        dollar_off = random.randrange(50)
        
        
        reg_form = EmailUserCreationForm(data=registration_form_data)
        self.user = reg_form.save()
        
        self.user.first_name = first_name
        self.user.last_name = last_name
        self.user.save()
        
        self.account = Account.create(self.user, self.user.email, self.user.first_name, self.user.last_name, '', 'en')
        self.assertTrue(self.account.recurly_account.state == 'active')
        self.assertTrue(self.account.hosted_login_url.find(self.account.hosted_login_token) >= 0)        

        unit_amount = decimal.Decimal(random.randrange(10000))/100
        quantity = random.randrange(10)
        adjustment = Adjustment.create(self.account, "Unit test.", unit_amount, quantity, 'USD', accounting_code='unittest')
        
        found_adjustment = False
        for recurly_adjustment in self.account.recurly_account.adjustments():
            if recurly_adjustment.uuid == adjustment.uuid: 
                self.assertTrue(recurly_adjustment.state == 'pending')
                found_adjustment = True
                break
        self.assertTrue(found_adjustment)
        
        adjustment = self.account.charge(gen_name(random.randrange(8,20)), decimal.Decimal(random.randrange(10000))/100, random.randrange(10), 'USD', 'adj2')
        found_adjustment = False
        for recurly_adjustment in self.account.recurly_account.adjustments():
            if recurly_adjustment.uuid == adjustment.uuid: 
                self.assertTrue(recurly_adjustment.state == 'pending')
                found_adjustment = True
                break
        self.assertTrue(found_adjustment)
        
        address1 = '{number} {street}'.format(number=random.randrange(20000), street=gen_name(random.randrange(4, 8)))
        address2 = ''
        city = gen_name(random.randrange(4, 8))
        state = 'CA'
        zipcode = '00001'
        country = 'US'
        phone = '123-123-1234'
        vat_number = ''
        ip_address = '127.0.0.1'
        number = '4111111111111111'
        verification_value = '123'
        month = 12
        year = 2020
        self.billing_info = BillingInfo.create(self.account, self.account.first_name, self.account.last_name, self.account.company_name, address1, address2, city, state, zipcode, country, phone, vat_number, ip_address, number, verification_value, month, year)
        
        self.assertTrue(self.billing_info.recurly_billing_info.last_four == '1111' == self.billing_info.last_four)
        
        percent_off_coupon = Coupon.create(percent_off_coupon_code, percent_off_coupon_name, discount_type='percent', discount_percent=percent_off, hosted_description='hosted coupon description', invoice_description='invoice coupon description', applies_to_all_plans=True)
        self.assertTrue(percent_off_coupon.state == percent_off_coupon.recurly_coupon.state == 'redeemable')
        
        dollar_off_coupon = Coupon.create(dollar_off_coupon_code, dollar_off_coupon_name, discount_type='dollars', discount_percent=dollar_off, hosted_description='hosted coupon description', invoice_description='invoice coupon description', applies_to_all_plans=True)
        
        coupon_redemption = CouponRedemption.create(percent_off_coupon, self.account, 'USD')
        self.assertTrue(self.account.recurly_account.redemption().coupon().coupon_code == percent_off_coupon.coupon_code)
        
        invoice = Invoice.create(self.account)
        self.assertTrue(invoice.invoice_number == invoice.recurly_invoice.invoice_number)
        
        plan_code = plan_name = plan_description = plan_accounting_code = gen_name(10)
        self.plan = Plan.create(plan_code, plan_name, plan_description, 39.99, accounting_code=plan_accounting_code)
        self.assertTrue(self.plan.recurly_plan.plan_code == self.plan.plan_code)
        
        plan_addon_code = addon_name = gen_name(10)
        plan_add_on = PlanAddOn.create(self.plan, plan_addon_code, addon_name, 9.99, default_quantity=1)
        found_addon = False
        for addon in self.plan.recurly_plan.add_ons():
            if addon.add_on_code == plan_addon_code:
                found_addon = True
                break
        self.assertTrue(found_addon)
        
        self.subscription = Subscription.create(self.plan, self.account)
        self.assertTrue(self.subscription.uuid == self.subscription.recurly_subscription.uuid)
        
        transaction = Transaction.create(self.account, decimal.Decimal(random.randrange(10000))/100, 'USD', 'unit test transaction')
        self.assertTrue(transaction.uuid == transaction.recurly_transaction.uuid)
        
        
        
        # clean up recurly stuff when finished.
        self.subscription.recurly_subscription.terminate(refund='none')
        self.account.recurly_account.delete()
        self.plan.recurly_plan.delete()
        dollar_off_coupon.recurly_coupon.delete()
        percent_off_coupon.recurly_coupon.delete()
        