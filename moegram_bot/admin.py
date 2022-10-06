from django.contrib import admin

from .models import TelegramUser


class TelegramUserAdmin(admin.ModelAdmin):
    list_display = (
        "user_id",
        "username",
        "first_name",
        "last_name",
        "is_active",
        "is_blocked",
    )

    search_fields = ["user_id", "first_name", "last_name", "username"]

    readonly_fields = ("created_at", "updated_at")


admin.site.register(TelegramUser, TelegramUserAdmin)
