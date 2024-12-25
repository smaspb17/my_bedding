from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInlineAdmin(admin.StackedInline):
    model = OrderItem
    fields = ['article', 'price', 'quantity']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'phone', 'email',
              'user_address', 'transport_company', 'pickup_point_address',
              'create_date', 'status', 'payment', 'coupon', 'discount_percentage',
              'total_cost', 'discount', 'delivery_cost', 'total_cost_after_discount']
    readonly_fields = ['create_date']
    list_editable = ['status', 'payment']
    list_display = ['id', 'create_date', 'phone', 'email', 'transport_company',
                    'pickup_point_address', 'status', 'payment', 'total_cost_after_discount']
    list_filter = ['create_date', 'status', 'payment']
    search_fields = ['id', 'first_name', 'last_name', 'phone', 'email',
                     'pickup_point_address']
    inlines = [OrderItemInlineAdmin,]
    save_on_top = True

