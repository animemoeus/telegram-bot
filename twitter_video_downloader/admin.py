from django.contrib import admin

from .models import TelegramUser


class TelegramUserAdmin(admin.ModelAdmin):
    pass


admin.site.register(TelegramUser, TelegramUserAdmin)
