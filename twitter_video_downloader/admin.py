from django.contrib import admin

from .models import TelegramUser, Tweet


class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "username", "request_count"]
    readonly_fields = [
        "user_id",
        "first_name",
        "last_name",
        "username",
        "request_count",
        "created_at",
        "updated_at",
    ]


class TweetAdmin(admin.ModelAdmin):
    pass


admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(Tweet, TweetAdmin)
