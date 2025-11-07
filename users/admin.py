from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'is_google_user', 'is_active', 'date_joined']
    list_filter = ['role', 'is_google_user', 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']

    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {'fields': ('role', 'is_google_user')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Adicional', {'fields': ('role', 'is_google_user')}),
    )
