# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Account'
        db.create_table('oscar_recurly_account', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('account_code', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=255)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('company_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('accept_language', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('hosted_login_token', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('oscar_recurly', ['Account'])

        # Adding model 'Adjustment'
        db.create_table('oscar_recurly_adjustment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oscar_recurly.Account'])),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=32, db_index=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('accounting_code', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('origin', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('unit_amount', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('quantity', self.gf('django.db.models.fields.IntegerField')()),
            ('discount', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('tax', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('total', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('taxable', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('invoice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oscar_recurly.Invoice'], null=True, blank=True)),
        ))
        db.send_create_signal('oscar_recurly', ['Adjustment'])

        # Adding model 'BillingInfo'
        db.create_table('oscar_recurly_billinginfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oscar_recurly.Account'])),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('company', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('address1', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('address2', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('vat_number', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('ip_address', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('ip_address_country', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('card_type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
            ('month', self.gf('django.db.models.fields.IntegerField')()),
            ('first_six', self.gf('django.db.models.fields.CharField')(max_length=6, null=True, blank=True)),
            ('last_four', self.gf('django.db.models.fields.CharField')(max_length=4, null=True, blank=True)),
            ('paypal_billing_agreement_id', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
        ))
        db.send_create_signal('oscar_recurly', ['BillingInfo'])

        # Adding model 'Coupon'
        db.create_table('oscar_recurly_coupon', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('coupon_code', self.gf('django.db.models.fields.CharField')(max_length=50, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('hosted_description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('invoice_description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('discount_type', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('discount_percent', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('discount_dollars', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('redeem_by_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('single_use', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('applies_for_months', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('max_redemptions', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('applies_to_all_plans', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('oscar_recurly', ['Coupon'])

        # Adding M2M table for field plans on 'Coupon'
        db.create_table('oscar_recurly_coupon_plans', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('coupon', models.ForeignKey(orm['oscar_recurly.coupon'], null=False)),
            ('plan', models.ForeignKey(orm['oscar_recurly.plan'], null=False))
        ))
        db.create_unique('oscar_recurly_coupon_plans', ['coupon_id', 'plan_id'])

        # Adding model 'CouponRedemption'
        db.create_table('oscar_recurly_couponredemption', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('coupon', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oscar_recurly.Coupon'])),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oscar_recurly.Account'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('single_use', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('total_discounted', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('oscar_recurly', ['CouponRedemption'])

        # Adding model 'Invoice'
        db.create_table('oscar_recurly_invoice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oscar_recurly.Account'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=32, db_index=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('invoice_number', self.gf('django.db.models.fields.IntegerField')()),
            ('po_number', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('vat_number', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('subtotal', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('tax', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('total', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('oscar_recurly', ['Invoice'])

        # Adding model 'Plan'
        db.create_table('oscar_recurly_plan', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('plan_code', self.gf('django.db.models.fields.CharField')(max_length=50, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('success_url', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('cancel_url', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('display_donation_amounts', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('display_quantity', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('display_phone_number', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('bypass_hosted_confirmation', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('unit_name', self.gf('django.db.models.fields.CharField')(default='users', max_length=20)),
            ('payment_page_tos_link', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('plan_interval_length', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('plan_interval_unit', self.gf('django.db.models.fields.CharField')(default='months', max_length=20)),
            ('trial_interval_length', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('trial_interval_unit', self.gf('django.db.models.fields.CharField')(default='months', max_length=20)),
            ('accounting_code', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('unit_amount', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('setup_fee', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=2)),
        ))
        db.send_create_signal('oscar_recurly', ['Plan'])

        # Adding model 'PlanAddOn'
        db.create_table('oscar_recurly_planaddon', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('plan', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oscar_recurly.Plan'])),
            ('add_on_code', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('display_quantity_on_hosted_page', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('default_quantity', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('unit_amount', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('oscar_recurly', ['PlanAddOn'])

        # Adding model 'Subscription'
        db.create_table('oscar_recurly_subscription', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oscar_recurly.Account'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('plan', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oscar_recurly.Plan'])),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=32, db_index=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('unit_amount', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('activated_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('canceled_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('expires_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('current_period_started_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('current_period_ends_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('trial_started_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('trial_ends_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('oscar_recurly', ['Subscription'])

        # Adding M2M table for field subscription_add_ons on 'Subscription'
        db.create_table('oscar_recurly_subscription_subscription_add_ons', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('subscription', models.ForeignKey(orm['oscar_recurly.subscription'], null=False)),
            ('planaddon', models.ForeignKey(orm['oscar_recurly.planaddon'], null=False))
        ))
        db.create_unique('oscar_recurly_subscription_subscription_add_ons', ['subscription_id', 'planaddon_id'])

        # Adding model 'Transaction'
        db.create_table('oscar_recurly_transaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oscar_recurly.Account'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('invoice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oscar_recurly.Invoice'], null=True, blank=True)),
            ('subscription', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oscar_recurly.Subscription'], null=True, blank=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('tax', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('test', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('voidable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('refundable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cvv_result', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('avs_result', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('avs_result_street', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('avs_result_postal', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('account_account_code', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('account_first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('account_last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('account_company', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('billing_info_first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('billing_info_last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('billing_info_address1', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('billing_info_address2', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('billing_info_city', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('billing_info_state', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('billing_info_zip', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('billing_info_country', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('billing_info_phone', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('billing_info_vat_number', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('billing_info_card_type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('billing_info_year', self.gf('django.db.models.fields.IntegerField')()),
            ('billing_info_month', self.gf('django.db.models.fields.IntegerField')()),
            ('billing_info_first_six', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('billing_info_last_four', self.gf('django.db.models.fields.CharField')(max_length=4)),
        ))
        db.send_create_signal('oscar_recurly', ['Transaction'])


    def backwards(self, orm):
        # Deleting model 'Account'
        db.delete_table('oscar_recurly_account')

        # Deleting model 'Adjustment'
        db.delete_table('oscar_recurly_adjustment')

        # Deleting model 'BillingInfo'
        db.delete_table('oscar_recurly_billinginfo')

        # Deleting model 'Coupon'
        db.delete_table('oscar_recurly_coupon')

        # Removing M2M table for field plans on 'Coupon'
        db.delete_table('oscar_recurly_coupon_plans')

        # Deleting model 'CouponRedemption'
        db.delete_table('oscar_recurly_couponredemption')

        # Deleting model 'Invoice'
        db.delete_table('oscar_recurly_invoice')

        # Deleting model 'Plan'
        db.delete_table('oscar_recurly_plan')

        # Deleting model 'PlanAddOn'
        db.delete_table('oscar_recurly_planaddon')

        # Deleting model 'Subscription'
        db.delete_table('oscar_recurly_subscription')

        # Removing M2M table for field subscription_add_ons on 'Subscription'
        db.delete_table('oscar_recurly_subscription_subscription_add_ons')

        # Deleting model 'Transaction'
        db.delete_table('oscar_recurly_transaction')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'oscar_recurly.account': {
            'Meta': {'ordering': "('-pk',)", 'object_name': 'Account'},
            'accept_language': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'account_code': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'hosted_login_token': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'oscar_recurly.adjustment': {
            'Meta': {'ordering': "('-pk',)", 'object_name': 'Adjustment'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oscar_recurly.Account']"}),
            'accounting_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'discount': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oscar_recurly.Invoice']", 'null': 'True', 'blank': 'True'}),
            'origin': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'tax': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'taxable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'total': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'unit_amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'})
        },
        'oscar_recurly.billinginfo': {
            'Meta': {'ordering': "('-pk',)", 'object_name': 'BillingInfo'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oscar_recurly.Account']"}),
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'card_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'first_six': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'ip_address_country': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'last_four': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'month': ('django.db.models.fields.IntegerField', [], {}),
            'paypal_billing_agreement_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'vat_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'oscar_recurly.coupon': {
            'Meta': {'ordering': "('coupon_code',)", 'object_name': 'Coupon'},
            'applies_for_months': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'applies_to_all_plans': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'coupon_code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'discount_dollars': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'discount_percent': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'discount_type': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'hosted_description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'max_redemptions': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'plans': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['oscar_recurly.Plan']", 'symmetrical': 'False'}),
            'redeem_by_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'single_use': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'oscar_recurly.couponredemption': {
            'Meta': {'ordering': "('-pk',)", 'object_name': 'CouponRedemption'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oscar_recurly.Account']"}),
            'coupon': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oscar_recurly.Coupon']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'single_use': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'total_discounted': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'oscar_recurly.invoice': {
            'Meta': {'ordering': "('-pk',)", 'object_name': 'Invoice'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oscar_recurly.Account']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_number': ('django.db.models.fields.IntegerField', [], {}),
            'po_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'subtotal': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'tax': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'total': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            'vat_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'oscar_recurly.plan': {
            'Meta': {'ordering': "('plan_code',)", 'object_name': 'Plan'},
            'accounting_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'bypass_hosted_confirmation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cancel_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'display_donation_amounts': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'display_phone_number': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'display_quantity': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'payment_page_tos_link': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'plan_code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'plan_interval_length': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'plan_interval_unit': ('django.db.models.fields.CharField', [], {'default': "'months'", 'max_length': '20'}),
            'setup_fee': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'}),
            'success_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'trial_interval_length': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'trial_interval_unit': ('django.db.models.fields.CharField', [], {'default': "'months'", 'max_length': '20'}),
            'unit_amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'unit_name': ('django.db.models.fields.CharField', [], {'default': "'users'", 'max_length': '20'})
        },
        'oscar_recurly.planaddon': {
            'Meta': {'ordering': "('plan', 'add_on_code')", 'object_name': 'PlanAddOn'},
            'add_on_code': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'default_quantity': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'display_quantity_on_hosted_page': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'plan': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oscar_recurly.Plan']"}),
            'unit_amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'})
        },
        'oscar_recurly.subscription': {
            'Meta': {'ordering': "('-pk',)", 'object_name': 'Subscription'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oscar_recurly.Account']"}),
            'activated_at': ('django.db.models.fields.DateTimeField', [], {}),
            'canceled_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'current_period_ends_at': ('django.db.models.fields.DateTimeField', [], {}),
            'current_period_started_at': ('django.db.models.fields.DateTimeField', [], {}),
            'expires_at': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'plan': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oscar_recurly.Plan']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'subscription_add_ons': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['oscar_recurly.PlanAddOn']", 'null': 'True', 'blank': 'True'}),
            'trial_ends_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'trial_started_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'unit_amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'})
        },
        'oscar_recurly.transaction': {
            'Meta': {'ordering': "('-pk',)", 'object_name': 'Transaction'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oscar_recurly.Account']"}),
            'account_account_code': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'account_company': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'account_first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'account_last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'action': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'avs_result': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'avs_result_postal': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'avs_result_street': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'billing_info_address1': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'billing_info_address2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'billing_info_card_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'billing_info_city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'billing_info_country': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'billing_info_first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'billing_info_first_six': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'billing_info_last_four': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'billing_info_last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'billing_info_month': ('django.db.models.fields.IntegerField', [], {}),
            'billing_info_phone': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'billing_info_state': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'billing_info_vat_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'billing_info_year': ('django.db.models.fields.IntegerField', [], {}),
            'billing_info_zip': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'cvv_result': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oscar_recurly.Invoice']", 'null': 'True', 'blank': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'refundable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'subscription': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oscar_recurly.Subscription']", 'null': 'True', 'blank': 'True'}),
            'tax': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'test': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'voidable': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['oscar_recurly']