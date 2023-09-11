from django.conf import settings
from django.db import models

from app.services import TelegramUserServicesV2


class TelegramUser(models.Model, TelegramUserServicesV2):
    TELEGRAM_BOT_TOKEN = settings.TVD_BOT_TOKEN

    user_id = models.CharField(max_length=25)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, default="")
    username = models.CharField(max_length=255, default="")

    is_active = models.BooleanField(default=True)
    request_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
