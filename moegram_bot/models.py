from email.policy import default
from random import choices

from django.db import models

from .telegram import send_text_message, send_typing_action


class TelegramUser(models.Model):
    class Interval(models.IntegerChoices):
        ZERO = 0
        ONE_MINUTE = 1
        FIVE_MINUTES = 5
        TEN_MINUTES = 10
        FIFTEEN_MINUTES = 15
        TWENTY_MINUTES = 20
        TWENTY_FIVE_MINUTES = 25
        THIRTY_MINUTES = 30
        THIRTY_FIVE_MINUTES = 35
        FORTY_MINUTES = 40
        FORTY_FIVE_MINUTES = 45
        FIFTY_MINUTES = 50
        FIFTY_FIVE_MINUTES = 55
        SIXTY_MINUTES = 60

    user_id = models.CharField(max_length=25)

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, default="")
    username = models.CharField(max_length=255, blank=True, default="")

    request_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=False)

    send_like_interval = models.IntegerField(choices=Interval.choices, default=60)
    last_send_like_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def send_typing_action(self):
        send_typing_action(self.user_id)

    def send_text_message(self, message=None, reply_to_message_id=None):
        send_text_message(
            user_id=self.user_id,
            message=message,
            reply_to_message_id=reply_to_message_id,
        )
