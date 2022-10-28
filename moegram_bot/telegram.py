import requests
from django.conf import settings


def send_typing_action(user_id):

    url = f"https://api.telegram.org/bot{settings.MOEGRAM_BOT_TOKEN}/sendChatAction"
    payload = {"chat_id": user_id, "action": "typing"}
    requests.request("POST", url, data=payload)


def send_text_message(user_id=None, reply_to_message_id=None, message=None):
    url = f"https://api.telegram.org/bot{settings.MOEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": user_id,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": "True",
        "disable_notification": "True",
        "reply_to_message_id": reply_to_message_id,
    }

    response = requests.request("POST", url, data=payload)

    if response.ok:
        pass
    else:
        pass
