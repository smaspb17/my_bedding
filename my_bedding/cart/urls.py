from django.urls import path


from .views import (cart_add, cart_detail, cart_remove,
                    cart_increase, cart_decrease, update_quantity,
                    get_discount)

app_name = 'cart'

urlpatterns = [
    path('', cart_detail, name='cart-detail'),
    path('add/<int:article>/', cart_add, name='cart-add'),
    path('remove/<int:article>/', cart_remove, name='cart-remove'),
    path('increase/<int:article>/', cart_increase, name='cart-increase'),
    path('decrease/<int:article>/', cart_decrease, name='cart-decrease'),
    path('update_quantity/<int:article>/', update_quantity, name='update-quantity'),
    # path('status/', cart_status, name='cart-status'),
    path('get_discount/', get_discount, name='get_discount'),
]