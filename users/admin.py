from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    # Show extra info in list view
    list_display = ("username", "email", "first_name", "last_name", "full_name", "is_staff")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("id",)

    # Add custom fields to fieldsets if needed (here we don't have extras)
    fieldsets = UserAdmin.fieldsets
    add_fieldsets = UserAdmin.add_fieldsets