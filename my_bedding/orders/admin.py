from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Order, OrderItem


class OrderItemInlineAdmin(admin.TabularInline):
    model = OrderItem
    fields = ['article', 'price', 'quantity']
    # readonly_fields = ['article', 'price', 'quantity']  # Поля только для чтения


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # form = OrderAdminForm
    fields = ['user', 'first_name', 'last_name', 'phone', 'email',
              'user_address', 'transport_company', 'pickup_point_address',
              'create_date', 'status', 'payment', 'coupon', 'discount_percentage',
              'total_cost', 'discount', 'delivery_cost', 'total_cost_after_discount']
    readonly_fields = ['create_date']
    # list_editable = ['status']
    list_display = ['id', 'create_date', 'status', 'transport_company',
                    'pickup_point_address', 'phone', 'total_cost_after_discount', 'payment',
                    'order_stripe_payment']
    list_filter = ['create_date', 'status', 'payment']
    search_fields = ['id', 'first_name', 'last_name', 'phone', 'email',
                     'pickup_point_address']
    inlines = [OrderItemInlineAdmin,]
    save_on_top = True

    @admin.display(description='Платеж Stripe')
    def order_stripe_payment(self, obj):
        url = obj.get_stripe_url()
        if obj.stripe_id:
            html = f'<a href="{url}" target="_blank">{obj.stripe_id}</a>'
            return mark_safe(html)
        return ''

    @staticmethod
    def user(obj):
        return obj.user.id




