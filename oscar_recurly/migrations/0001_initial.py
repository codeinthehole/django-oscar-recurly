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
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('accounting_code', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
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
            ('vat_number', self.gf('django.db.models.fields.CharField')(max_length=20)),
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
        ))
        db.send_create_signal('oscar_recurly', ['CouponRedemption'])

        # Adding model 'Invoice'
        db.create_table('oscar_recurly_invoice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('oscar_recurly', ['Invoice'])

        # Adding model 'Plan'
        db.create_table('oscar_recurly_plan', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('oscar_recurly', ['Plan'])

        # Adding model 'PlanAddOn'
        db.create_table('oscar_recurly_planaddon', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('oscar_recurly', ['PlanAddOn'])

        # Adding model 'Subscription'
        db.create_table('oscar_recurly_subscription', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('oscar_recurly', ['Subscription'])

        # Adding model 'Transaction'
        db.create_table('oscar_recurly_transaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('oscar_recurly', ['Transaction'])

        # Adding model 'OrderTransaction'
        db.create_table('oscar_recurly_ordertransaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order_number', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, db_index=True)),
            ('txn_type', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('txn_ref', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=2, blank=True)),
            ('response_code', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('response_message', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('request_xml', self.gf('django.db.models.fields.TextField')()),
            ('response_xml', self.gf('django.db.models.fields.TextField')()),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('oscar_recurly', ['OrderTransaction'])


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

        # Deleting model 'Transaction'
        db.delete_table('oscar_recurly_transaction')

        # Deleting model 'OrderTransaction'
        db.delete_table('oscar_recurly_ordertransaction')


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
            'Meta': {'object_name': 'Account'},
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
            'Meta': {'object_name': 'Adjustment'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oscar_recurly.Account']"}),
            'accounting_code': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'discount': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'origin': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'tax': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'taxable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'total': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'unit_amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'oscar_recurly.billinginfo': {
            'Meta': {'object_name': 'BillingInfo'},
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
            'vat_number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'year': ('django.db.models.fields.IntegerField', [], {}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'oscar_recurly.coupon': {
            'Meta': {'object_name': 'Coupon'},
            'applies_for_months': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'applies_to_all_plans': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'coupon_code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
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
            'Meta': {'object_name': 'CouponRedemption'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'oscar_recurly.invoice': {
            'Meta': {'object_name': 'Invoice'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'oscar_recurly.ordertransaction': {
            'Meta': {'ordering': "('-date_created',)", 'object_name': 'OrderTransaction'},
            'amount': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '2', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order_number': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'db_index': 'True'}),
            'request_xml': ('django.db.models.fields.TextField', [], {}),
            'response_code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'response_message': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'response_xml': ('django.db.models.fields.TextField', [], {}),
            'txn_ref': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'txn_type': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        },
        'oscar_recurly.plan': {
            'Meta': {'object_name': 'Plan'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'oscar_recurly.planaddon': {
            'Meta': {'object_name': 'PlanAddOn'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'oscar_recurly.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'oscar_recurly.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['oscar_recurly']