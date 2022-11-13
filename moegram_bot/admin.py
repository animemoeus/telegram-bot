from django.contrib import admin

from .models import TelegramUser


class TelegramUserAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "username",
        "is_blocked",
        "request_count",
        "updated_at",
    )

    search_fields = ["user__username"]

    readonly_fields = (
        "user",
        "username",
        "request_count",
        "last_send_like_date",
        "created_at",
        "updated_at",
    )


admin.site.register(TelegramUser, TelegramUserAdmin)
