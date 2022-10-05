from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import TelegramUser
from .utils import send_like

import json


def index(request):
    return HttpResponse("Hello, world")


@csrf_exempt
def telegram_webhook_v1(request):

    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except:
            return HttpResponse("ლ(╹◡╹ლ)")

        # get Telegram user information
        user = {
            "user_id": data["message"]["from"]["id"],
            "first_name": data["message"]["from"]["first_name"],
            "last_name": data["message"]["from"]["last_name"]
            if data["message"]["from"].__contains__("last_name")
            else "",
            "username": data["message"]["from"]["username"]
            if data["message"]["from"].__contains__("username")
            else "",
        }
        message = {
            "type": "text" if data["message"].__contains__("text") else "unknown",
            "id": data["message"]["message_id"],
        }

        if message["type"] == "text":
            message["text"] = data["message"]["text"]

        # create or update TelegramUser
        telegram_user, created = TelegramUser.objects.update_or_create(
            user_id=user["user_id"], defaults=(user)
        )
        telegram_user.request_count += 1
        telegram_user.save()

        # hanlde blocked TelegramUser
        if telegram_user.is_blocked:
            telegram_user.send_text_message(
                message="Your account is already blocked (〜￣▽￣)〜",
                reply_to_message_id=message["id"],
            )

        if message["type"] == "text":
            if message["text"] == "/start":
                telegram_user.send_typing_action()

                telegram_user.send_text_message(
                    message=f"Hello {telegram_user.first_name} 😁\n\nWelcome to Moegram Bot!",
                    reply_to_message_id=message["id"],
                )

                telegram_user.send_text_message(
                    message=f"Type /help to start using Moegram Bot!",
                )

            elif message["text"] == "/help":
                telegram_user.send_typing_action()

                telegram_user.send_text_message(
                    message=f"Send your Instagram post URL here to increse your post like 💗",
                    reply_to_message_id=message["id"],
                )

                telegram_user.send_text_message(
                    message=f"Note: Make sure that your Instagram account not private.",
                )

            elif message["text"].startswith("https://www.instagram.com/"):
                like_status = send_like(message["text"])

                if like_status:
                    telegram_user.send_typing_action()
                    telegram_user.send_text_message(
                        message=f"Likes sent successfully (. ❛ ᴗ ❛.)",
                        reply_to_message_id=message["id"],
                    )
                else:
                    telegram_user.send_typing_action()
                    telegram_user.send_text_message(
                        message=f"Likes failed to send (┬┬﹏┬┬)",
                        reply_to_message_id=message["id"],
                    )
        else:
            telegram_user.send_text_message(
                message="Invalid message ლ(╹◡╹ლ)", reply_to_message_id=message["id"]
            )

        return HttpResponse("arter tendean")
