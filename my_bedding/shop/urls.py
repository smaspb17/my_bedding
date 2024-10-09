from django.urls import path

from . import views

app_name = 'shop'


urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('catalog/', views.catalog_list, name='cat_list'),
    path('catalog/<slug:cat_slug>/', views.product_list,
         name='product_list_by_cat'),
    path('catalog/<slug:cat_slug>/<int:product_id>/',
         views.product_detail, name='product_detail'),
    path('test/', views.test_view, name='test'),
]
