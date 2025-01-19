from django.contrib.auth.views import PasswordChangeView
from django.urls import path

from .views import (get_csrf_token, register, login_user, logout_user, view_account, edit_account,
                    PasswordResetAjaxView, PasswordResetConfirmAjaxView, update_photo, delete_photo)

app_name = 'users'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('login-html/', login_user, name='login_html'),
    path('logout/', logout_user, name='logout'),
    path('account/', view_account, name='view_account'),
    path('account/edit/', edit_account, name='edit_account'),
    path('get-csrf-token/', get_csrf_token, name='get_csrf_token'),
    path('password-reset/', PasswordResetAjaxView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmAjaxView.as_view(),
         name='password_reset_confirm'),
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('update-photo/', update_photo, name='update_photo'),
    path('delete-photo/', delete_photo, name='delete_photo'),
]
