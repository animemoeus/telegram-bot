import json

import requests


class TelegramUserServices:
    TELEGRAM_BOT_TOKEN = None

    def send_typing_action(self):
        url = f"https://api.telegram.org/bot{self.TELEGRAM_BOT_TOKEN}/sendChatAction"
        payload = {"chat_id": self.user_id, "action": "typing"}
        requests.request("POST", url, data=payload)

    def send_upload_video_action(self):
        url = f"https://api.telegram.org/bot{self.TELEGRAM_BOT_TOKEN}/sendChatAction"
        payload = {"chat_id": self.user_id, "action": "upload_video"}
        requests.request("POST", url, data=payload)

    def send_text_message(self, message: str, message_id: int = None):
        url = f"https://api.telegram.org/bot{self.TELEGRAM_BOT_TOKEN}/sendMessage"

        payload = {
            "chat_id": self.user_id,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": "True",
            "disable_notification": "True",
            "reply_to_message_id": message_id,
        }

        self.send_typing_action()
        requests.request("POST", url, data=payload)

    def send_video(self, caption: str, videos: list):
        self.send_upload_video_action()

        url = f"https://api.telegram.org/bot{self.TELEGRAM_BOT_TOKEN}/sendVideo"
        payload = json.dumps(
            {
                "chat_id": self.user_id,
                "video": videos[0]["url"],
                "caption": caption,
                "parse_mode": "HTML",
                "reply_to_message_id": "message_id",
                "reply_markup": {
                    "inline_keyboard": [
                        [
                            {"text": f'🔗 {video["size"]}', "url": video["url"]}
                            for video in videos
                        ],
                    ]
                },
            }
        )
        headers = {"Content-Type": "application/json"}

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.ok
