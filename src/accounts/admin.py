from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import *

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'phone_number', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'password')}),
        (_('Permissions'), {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

    search_fields = ('email', 'phone_number')
    ordering = ('email',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_pic', 'created_at', 'updated_at')
    search_fields = ('user__email', 'user__phone_number')
    list_filter = ('created_at', 'updated_at')

    fieldsets = (
        (None, {'fields': ('user', 'profile_pic')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user', 'profile_pic')}
        ),
    )
    search_fields = ('user__email', 'user__phone_number')
    ordering = ('user__email',)
    filter_horizontal = ()
    