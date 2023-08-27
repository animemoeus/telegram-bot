import json


class TelegramWebhookHandler:
    """
    This class will be used to handle the Telegram webhook data from post request methods.
    """

    def __init__(self, request: bytes):
        self.request = request
        self.data = None

    @property
    def is_valid(self) -> bool:
        """Returns true or false"""

        try:
            self.data = json.loads(self.request)
            return True
        except:
            return False

    def get_user_data(self) -> dict:
        """
        This method will return the dictionary of Telegram user data.
        https://core.telegram.org/bots/api#user.
        """

        if not self.is_valid:
            return {}

        user_data = {}

        if self.data and self.data.get("message"):
            user_data["id"] = self.data["message"]["from"]["id"]
            user_data["first_name"] = self.data["message"]["from"]["first_name"]
            user_data["last_name"] = (
                self.data["message"]["from"]["last_name"]
                if self.data["message"]["from"]["last_name"]
                else ""
            )
            user_data["username"] = (
                self.data["message"]["from"]["username"]
                if self.data["message"]["from"]["username"]
                else ""
            )
            user_data["language_code"] = (
                self.data["message"]["from"]["language_code"]
                if self.data["message"]["from"]["language_code"]
                else "en"
            )

        return user_data
