from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from .telegram import send_text_message, send_typing_action


class TelegramUser(models.Model):
    class Interval(models.IntegerChoices):
        UNLIMITED = 0
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

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=255, blank=True, default="")

    request_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_blocked = models.BooleanField(default=False)

    send_like_interval = models.IntegerField(choices=Interval.choices, default=60)
    last_send_like_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def send_typing_action(self):
        send_typing_action(self.user.username)

    def send_text_message(self, message=None, reply_to_message_id=None):
        send_text_message(
            user_id=self.user.username,
            message=message,
            reply_to_message_id=reply_to_message_id,
        )

    @property
    def can_send_like(self):
        if (
            not self.last_send_like_date
            or self.last_send_like_date + timedelta(minutes=self.send_like_interval)
            < timezone.now()
        ):
            return True

        return False

    @property
    def get_waiting_time(self):
        waiting_time = (
            self.last_send_like_date + timedelta(minutes=self.send_like_interval)
        ) - timezone.now()
        waiting_time = timedelta(seconds=waiting_time.seconds)
        waiting_time = str(waiting_time).split(":")

        return f"Please wait {int(waiting_time[1])} {'minutes' if int(waiting_time[1]) > 1 else 'minute'} and {int(waiting_time[2])} {'seconds' if int(waiting_time[2])> 1 else 'second'}  :)"


class InstagramPost(models.Model):

    user = models.ForeignKey("TelegramUser", on_delete=models.CASCADE)

    url = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url
