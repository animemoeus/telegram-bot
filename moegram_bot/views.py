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
        }

        # create or update TelegramUser
        telegram_user, created = TelegramUser.objects.update_or_create(
            user_id=user["user_id"], defaults=(user)
        )
        telegram_user.request_count += 1
        telegram_user.save()

        # hanlde blocked TelegramUser
        if telegram_user.is_blocked:
            telegram_user.send_text_message(
                message="Your account is already blocked (〜￣▽￣)〜"
            )

        return HttpResponse("arter tendean")
