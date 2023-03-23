import requests


class TelegramUserServices:
    TELEGRAM_BOT_TOKEN = None

    def send_typing_action(self):
        url = f"https://api.telegram.org/bot{self.TELEGRAM_BOT_TOKEN}/sendChatAction"
        payload = {"chat_id": self.user.username, "action": "typing"}
        requests.request("POST", url, data=payload)

    def send_text_message(self, message: str, message_id: int = None):
        url = f"https://api.telegram.org/bot{self.TELEGRAM_BOT_TOKEN}/sendMessage"

        payload = {
            "chat_id": self.user.username,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": "True",
            "disable_notification": "True",
            "reply_to_message_id": message_id,
        }

        self.send_typing_action()
        requests.request("POST", url, data=payload)
