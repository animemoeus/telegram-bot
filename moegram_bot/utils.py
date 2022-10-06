import requests
from django.conf import settings


def send_like(post_url):
    url = f"{settings.LIKE_API_URL}"

    payload = {
        "api_key": "",
        "secret_key": "",
        "action": "order",
        "service": "4875",
        "data": post_url,
        "quantity": "50",
    }

    response = requests.request("POST", url, data=payload)

    return response.ok
