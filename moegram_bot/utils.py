import json

import requests
from django.conf import settings


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
