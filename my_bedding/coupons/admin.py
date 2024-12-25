from django.contrib import admin

from coupons.models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    fields = ['code', 'valid_from', 'valid_to',
              'discount', 'active']
    list_filter = ['active']
    list_display = ['code', 'valid_from', 'valid_to',
                    'discount', 'active']
    search_fields = ['code']
    list_editable = ['active']
