from email.policy import default
from django.db import models

from .telegram import send_typing_action, send_text_message


class TelegramUser(models.Model):
    user_id = models.CharField(max_length=25)

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, default="")
    username = models.CharField(max_length=255, blank=True, default="")

    request_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=False)

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
