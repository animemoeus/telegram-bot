import json
import random
from datetime import timedelta

from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from tabulate import tabulate

from .models import TelegramUser
from .utils import send_like


def index(request):
    return HttpResponse("Hello, world")


@csrf_exempt
def telegram_webhook(request):

    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # reject all incoming webhook without secret token
            if (
                request.headers.get("X-Telegram-Bot-Api-Secret-Token", None)
                != settings.MASTER_KEY_ACTIVATION
            ):
                return HttpResponse(".")

            if data.__contains__("edited_message"):
                return HttpResponse(".")
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

        # get message from Telegram user
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
            telegram_user.send_typing_action()
            telegram_user.send_text_message(
                message="Your account is already blocked (〜￣▽￣)〜",
                reply_to_message_id=message["id"],
            )
            return HttpResponse(".")

        # message to activate TelegramUser without admin page
        try:
            if message["text"] == settings.MASTER_KEY_ACTIVATION:
                telegram_user.send_typing_action()
                telegram_user.send_text_message(
                    message=f"Hello {telegram_user.first_name}, your account is activated(. ❛ ᴗ ❛.)",
                    reply_to_message_id=message["id"],
                )
                telegram_user.is_active = True
                telegram_user.save()
        except:
            pass

        # handle inactive TelegramUser
        if not telegram_user.is_active:
            telegram_user.send_typing_action()
            telegram_user.send_text_message(
                message=f"Contact @artertendean to activate your account 😁👍",
                reply_to_message_id=message["id"],
            )
            return HttpResponse(".")

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

            elif message["text"] == "arter":
                telegram_user.send_typing_action()

                telegram_user.send_text_message(
                    message=f"Dondon...",
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

            elif message["text"] == "/me":
                table = [
                    ["Name", telegram_user.first_name],
                    ["ID", telegram_user.user_id],
                ]
                msg = tabulate(table, tablefmt="plain")

                telegram_user.send_typing_action()
                telegram_user.send_text_message(
                    message=f"<pre>{msg}</pre>",
                    reply_to_message_id=message["id"],
                )

            elif message["text"].startswith("https://www.instagram.com/p/"):
                # if telegram user last send like time is None
                # or telegram user (last send like datetime + send like interval) less than current datetime
                # allow telegram user to send like
                if (
                    telegram_user.last_send_like_date is None
                    or telegram_user.last_send_like_date
                    + timedelta(minutes=telegram_user.send_like_interval)
                    < timezone.now()
                ):
                    # send like to Instagram post
                    like_status = send_like(message["text"])

                    if like_status == True:
                        telegram_user.send_typing_action()
                        telegram_user.send_text_message(
                            message=f"Likes sent successfully (. ❛ ᴗ ❛.)",
                            reply_to_message_id=message["id"],
                        )

                        # don't forget to update telegram user last send like date if like successfully sent
                        telegram_user.last_send_like_date = timezone.now()
                        telegram_user.save()
                    else:
                        telegram_user.send_typing_action()
                        telegram_user.send_text_message(
                            message=f"Likes failed to send (┬┬﹏┬┬)",
                            reply_to_message_id=message["id"],
                        )
                        telegram_user.send_text_message(
                            message=f"Try again later 😁👍",
                        )
                else:  # wait n of time before sending like again
                    # calculate waiting time
                    # idk how can i calculate the time, but it works 🤣
                    wait_time = (
                        telegram_user.last_send_like_date
                        + timedelta(minutes=telegram_user.send_like_interval)
                    ) - timezone.now()
                    wait_time = timedelta(seconds=wait_time.seconds)
                    wait_time = str(wait_time).split(":")

                    telegram_user.send_typing_action()
                    telegram_user.send_text_message(
                        message=f"Wait {int(wait_time[1])} {'minutes' if int(wait_time[1]) > 1 else 'minute'} {int(wait_time[2])} {'seconds' if int(wait_time[2])> 1 else 'second'} before sending like again :)",
                        reply_to_message_id=message["id"],
                    )
            else:
                telegram_user.send_typing_action()
                telegram_user.send_text_message(
                    message=f"{random.choice(['(. ❛ ᴗ ❛.)','(〜￣▽￣)〜','(￣o￣) . z Z'])}",
                    reply_to_message_id=message["id"],
                )
        else:
            telegram_user.send_typing_action()
            telegram_user.send_text_message(
                message="Invalid message ლ(╹◡╹ლ)", reply_to_message_id=message["id"]
            )

        return HttpResponse("arter tendean")
