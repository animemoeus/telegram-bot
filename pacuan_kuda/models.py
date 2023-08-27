from django.db import models

from app.services import TelegramUserServices


class TelegramUser(models.Model, TelegramUserServices):
    pass
