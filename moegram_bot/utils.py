import json

import requests
from django.conf import settings
from django.contrib.auth.models import User

from .models import TelegramUser


def send_like(post_url):
    url = settings.LIKE_API_URL

    payload = {
        "api_key": settings.LIKE_API_KEY,
        "secret_key": settings.LIKE_API_SECRET,
        "action": "order",
        "service": "4875",
        "data": post_url,
        "quantity": "50",
    }

    response = requests.request("POST", url, data=payload)

    response = json.loads(response.text)

    return response["status"]


def get_or_create_telegram_user(data):
    django_user, _ = User.objects.update_or_create(
        username=data["id"],
        defaults={
            "first_name": data["first_name"],
            "last_name": data["last_name"],
        },
    )

    telegram_user, _ = TelegramUser.objects.update_or_create(
        user=django_user,
        defaults=({"user": django_user, "username": data["username"]}),
    )

    return telegram_user
