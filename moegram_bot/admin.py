from django.contrib import admin

from .models import InstagramPost, TelegramUser


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
        "send_like_datetime",
        "created_at",
        "updated_at",
    )


class InstagramPostAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "url",
        "created_at",
    )

    readonly_fields = (
        "user",
        "url",
        "created_at",
    )


admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(InstagramPost, InstagramPostAdmin)
