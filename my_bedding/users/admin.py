from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import Profile


User = get_user_model()


class ProfileAdmin(admin.StackedInline):
    model = Profile
    fields = ['telegram_id', 'photo']
    can_delete = False
    verbose_name_plural = 'profile'


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email',)}),
        ('Личная информация', {'fields': ('first_name', 'last_name',
                                          'phone_number', 'address')}),
        ('Разрешения', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                   'groups', 'user_permissions'), }),
        ('Важные даты', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',),
        }),
    )
    list_display = ['id', 'email', 'first_name', 'last_name',
                    'phone_number', 'address']
    list_display_links = ['id', 'email']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups']
    search_fields = ['id', 'email', 'first_name', 'last_name',
                     'phone_number', 'address']
    ordering = ['-id',]
    filter_horizontal = ['groups', 'user_permissions']
    readonly_fields = ['last_login']
    inlines = [ProfileAdmin]


# # Переименовываем "Группы" в админке
# admin.site.unregister(Group)
#
#
# @admin.register(Group)
# class GroupAdmin(admin.ModelAdmin):
#     verbose_name = "Группа"
#     verbose_name_plural = "Группы"








