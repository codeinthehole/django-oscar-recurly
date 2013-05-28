from django.contrib import admin

from .models import *

admin.site.register(Account)
admin.site.register(Adjustment)
admin.site.register(BillingInfo)
admin.site.register(Coupon)
admin.site.register(CouponRedemption)
admin.site.register(Invoice)
admin.site.register(Plan)
admin.site.register(PlanAddOn)
admin.site.register(Subscription)
admin.site.register(Transaction)