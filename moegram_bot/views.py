from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import TelegramUser

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
        else:
            telegram_user.send_text_message(
                message="Invalid message ლ(╹◡╹ლ)", reply_to_message_id=message["id"]
            )

        return HttpResponse("arter tendean")
