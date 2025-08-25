from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User

    list_display = ("username", "email", "is_staff", "is_active", "role")
    list_filter = ("role", "is_staff", "is_active")

    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {"fields": ("role",)}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {"fields": ("role",)}),
    )

    search_fields = ("username", "email")
    ordering = ("username",)
