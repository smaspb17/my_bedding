from django.urls import path

from .views import coupon_apply, coupon_remove

app_name = 'coupons'


urlpatterns = [
    path('apply/', coupon_apply, name='apply'),
    path('remove/', coupon_remove, name='remove'),
]