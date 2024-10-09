from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Profile


User = get_user_model()


class ProfileAdmin(admin.StackedInline):
    model = Profile
    fields = ['telegram_id', 'photo']


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'username',)}),
        ('Личная информация', {'fields': ('first_name', 'last_name',
                                          'phone_number', 'address')}),
        ('Разрешения', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                   'groups', 'user_permissions'), }),
        ('Важные даты', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2',),
        }),
    )
    list_display = ['id', 'username', 'email', 'phone_number', 'address']
    list_display_links = ['id', 'username']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups']
    search_fields = ['id', 'username', 'first_name', 'last_name', 'email',
                     'phone_number', 'address']
    ordering = ['-id',]
    filter_horizontal = ['groups', 'user_permissions']
    readonly_fields = ['last_login']
    inlines = [ProfileAdmin]










