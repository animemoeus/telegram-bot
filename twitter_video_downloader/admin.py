from django.contrib import admin

from .models import TelegramUser, Tweet


class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "username", "request_count"]
    search_fields = ["first_name", "last_name", "username"]
    readonly_fields = [
        "user_id",
        "first_name",
        "last_name",
        "username",
        "request_count",
        "created_at",
        "updated_at",
    ]

    def has_add_permission(self, request, obj=None):
        return False


class TweetAdmin(admin.ModelAdmin):
    ordering = ["-created_at"]

    list_display = ["id", "created_at"]
    readonly_fields = ["created_at", "updated_at", "send_to", "data"]

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(Tweet, TweetAdmin)
