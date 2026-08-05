from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "telegram_id",
        "is_premium",
        "is_staff",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Extra Info",
            {
                "fields": (
                    "telegram_id",
                    "is_premium",
                )
            }
        ),
    )