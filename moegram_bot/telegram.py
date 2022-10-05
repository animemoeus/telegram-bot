import requests


def send_text_message(user_id=None, reply_to_message_id=None, message=None):
    url = "https://api.telegram.org/bot1421107253:AAEKZzGV5izwIINbURy5r-eH-Vk2e_eoOeY/sendMessage"

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
