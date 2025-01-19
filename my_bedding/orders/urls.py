from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('status/<int:order_id>', views.order_status, name='order_status'),
]
