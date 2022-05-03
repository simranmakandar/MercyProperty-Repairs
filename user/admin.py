from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ExtUser


class ExtUserAdmin(UserAdmin):
    model = ExtUser
    list_display = ['username', 'email', 'skillset', 'contact_no', 'user_role', 'is_manager', 'is_worker', 'is_staff',
                    'is_superuser']
    list_filter = ['username', 'email', 'is_manager', 'is_worker', 'skillset', 'is_staff', 'is_superuser']

    actions = ['enable_manager', 'disable_manager', 'enable_worker', 'disable_worker']

    def enable_manager(self, requst, queryset):
        queryset.update(is_manager=True)

    def disable_manager(self, requst, queryset):
        queryset.update(is_manager=False)

    def enable_worker(self, requst, queryset):
        queryset.update(is_worker=True)

    def disable_worker(self, requst, queryset):
        queryset.update(is_worker=False)

    enable_manager.short_description = "Enable the Manager Post"
    disable_manager.short_description = "Disable the Manager Post"

    enable_worker.short_description = "Enable the Worker Post"
    disable_worker.short_description = "Disable the Worker Post"

    fieldsets = (
        ('Account Information', {
            'fields': ('username', 'password', 'is_staff', 'is_superuser')
        }),
        ('Position', {
            'fields': ('skillset', 'user_role', 'is_manager', 'is_worker')
        }),
        ('Contact Information', {
            'fields': ('email', 'contact_no')
        })
    )
    add_fieldsets = (
        ('Account Information', {
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_superuser')
        }),
        ('Position', {
            'fields': ('skillset', 'user_role', 'is_manager', 'is_worker')
        }),
        ('Contact Information', {
            'fields': ('email', 'contact_no')
        })
    )


admin.site.register(ExtUser, ExtUserAdmin)
