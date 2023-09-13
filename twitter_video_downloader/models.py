import json
import uuid

import requests
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


class Tweet(models.Model):
    TELEGRAM_BOT_TOKEN = settings.TVD_BOT_TOKEN

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    send_to = models.CharField(
        max_length=25, help_text="Should contain Telegram user id"
    )

    data = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}"

    def send_video_to_user(self):
        url = f"https://api.telegram.org/bot{self.TELEGRAM_BOT_TOKEN}/sendVideo"
        payload = json.dumps(
            {
                "chat_id": self.send_to,
                "video": self.data.get("videos")[0]["url"],
                "caption": "",
                "parse_mode": "HTML",
                "reply_to_message_id": "",
                "reply_markup": {
                    "inline_keyboard": [
                        [
                            {"text": f'🔗 {video["size"]}', "url": video["url"]}
                            for video in self.data.get("videos")
                        ],
                    ]
                },
            }
        )
        headers = {"Content-Type": "application/json"}

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.ok
