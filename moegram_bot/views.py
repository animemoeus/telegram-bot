import json
import random

from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from tabulate import tabulate

from .models import InstagramPost, TelegramUser
from .serializers import TelegramUserSerializer
from .utils import get_or_create_telegram_user, send_like


def index(request):
    return HttpResponse("Hello, world")


# @csrf_exempt
# @api_view(["POST"])
# def telegram_webhook(request):

#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             print(data)
#             print(request.headers.get("X-Telegram-Bot-Api-Secret-Token", None))

#             # reject all incoming webhook without secret token
#             if (
#                 request.headers.get("X-Telegram-Bot-Api-Secret-Token", None)
#                 != settings.MASTER_KEY_ACTIVATION
#             ):
#                 return HttpResponse(".")

#             if data.__contains__("edited_message"):
#                 return HttpResponse(".")
#         except:
#             return HttpResponse("ლ(╹◡╹ლ)")

#         # get Telegram user information
#         user = {
#             "user_id": data["message"]["from"]["id"],
#             "first_name": data["message"]["from"]["first_name"],
#             "last_name": data["message"]["from"]["last_name"]
#             if data["message"]["from"].__contains__("last_name")
#             else "",
#             "username": data["message"]["from"]["username"]
#             if data["message"]["from"].__contains__("username")
#             else "",
#         }

#         # get or create django_user
#         try:
#             django_user = User.objects.get(username=user["user_id"])
#         except:
#             django_user = User.objects.create_user(username=user["user_id"])

#         # create or update telegram_user
#         telegram_user, _ = TelegramUser.objects.update_or_create(
#             user=django_user,
#             defaults=({"user": django_user, "username": user["username"]}),
#         )

#         telegram_user.user.first_name = user["first_name"]
#         telegram_user.user.last_name = user["last_name"]
#         telegram_user.request_count += 1
#         telegram_user.user.save()
#         telegram_user.save()

#         # get message from Telegram user
#         message = {
#             "type": "text" if data["message"].__contains__("text") else "unknown",
#             "id": data["message"]["message_id"],
#         }

#         if message["type"] == "text":
#             message["text"] = data["message"]["text"]

#         # hanlde blocked TelegramUser
#         if telegram_user.is_blocked:
#             telegram_user.send_typing_action()
#             telegram_user.send_text_message(
#                 message="Your account is already blocked (〜￣▽￣)〜",
#             )
#             return HttpResponse(".")

#         if message["type"] == "text":
#             if message["text"] == "/start":
#                 telegram_user.send_typing_action()

#                 telegram_user.send_text_message(
#                     message=f"Hello {telegram_user.user.first_name} 😁\n\nWelcome to Moegram Bot!",
#                     reply_to_message_id=message["id"],
#                 )

#                 telegram_user.send_text_message(
#                     message=f"Type /help to start using Moegram Bot!",
#                 )

#             elif message["text"] == "/help":
#                 telegram_user.send_typing_action()

#                 telegram_user.send_text_message(
#                     message=f"Send your Instagram post URL here to increase your post like ❤️‍🔥",
#                     reply_to_message_id=message["id"],
#                 )

#                 telegram_user.send_text_message(
#                     message=f"Note: Make sure that your Instagram account is not private.",
#                 )

#             elif message["text"] == "/me":
#                 telegram_user.send_typing_action()

#                 table = [
#                     [
#                         "Name",
#                         ":",
#                         f"{telegram_user.user.first_name} {telegram_user.user.last_name}",
#                     ],
#                     ["ID", ":", telegram_user.user.username],
#                 ]
#                 msg = tabulate(table, tablefmt="plain")

#                 telegram_user.send_text_message(
#                     message=f"<pre>{msg}</pre>",
#                     reply_to_message_id=message["id"],
#                 )

#             elif (
#                 message["text"].startswith("https://www.instagram.com/p/")
#                 or message["text"].startswith("https://www.instagram.com/reel/")
#                 or message["text"].startswith("https://www.instagram.com/tv/")
#             ):
#                 if telegram_user.can_send_like:
#                     # send like to Instagram post
#                     like_status = send_like(message["text"])

#                     if like_status == True:
#                         InstagramPost(user=telegram_user, url=message["text"]).save()

#                         telegram_user.send_typing_action()
#                         telegram_user.send_text_message(
#                             message=f"Likes sent successfully (. ❛ ᴗ ❛.)",
#                             reply_to_message_id=message["id"],
#                         )

#                         # don't forget to update telegram user last send like date if like successfully sent
#                         telegram_user.last_send_like_date = timezone.now()
#                         telegram_user.save()
#                     else:
#                         telegram_user.send_typing_action()
#                         telegram_user.send_text_message(
#                             message=f"Likes failed to send (┬┬﹏┬┬)",
#                             reply_to_message_id=message["id"],
#                         )
#                         telegram_user.send_text_message(
#                             message=f"Try again later 😁👍",
#                         )
#                 else:

#                     telegram_user.send_typing_action()
#                     telegram_user.send_text_message(
#                         message=telegram_user.get_waiting_time,
#                         reply_to_message_id=message["id"],
#                     )
#             else:
#                 telegram_user.send_typing_action()
#                 telegram_user.send_text_message(
#                     message=f"{random.choice(['(. ❛ ᴗ ❛.)','(〜￣▽￣)〜','(￣o￣) . z Z'])}",
#                     reply_to_message_id=message["id"],
#                 )
#         else:
#             telegram_user.send_typing_action()
#             telegram_user.send_text_message(
#                 message="Invalid message ლ(╹◡╹ლ)", reply_to_message_id=message["id"]
#             )

#         return HttpResponse("arter tendean")


class TelegramWebhookV2(APIView):
    def post(self, request):
        telegram_user_serializer = TelegramUserSerializer(
            data=request.data.get("message", {}).get("from", {})
            or request.data.get("edited_message", {}).get("from", {})
        )
        telegram_user_serializer.is_valid(raise_exception=True)
        telegram_user = get_or_create_telegram_user(telegram_user_serializer.data)

        if telegram_user.is_blocked:
            telegram_user.send_text_message("Fuck you!")
            return Response()

        user_message = request.data.get("message", {}).get("text")
        if not user_message:
            telegram_user.send_text_message("Can't process this message.")
            return Response()

        if user_message.startswith("/start"):
            telegram_user.send_text_message(
                message=f"Hello {telegram_user.user.first_name} 😁\n\nWelcome to Moegram Bot!",
            )
            telegram_user.send_text_message(
                message=f"Type /help to start using Moegram Bot!",
            )
        elif user_message.startswith("/help"):
            telegram_user.send_text_message(
                message=f"Send your Instagram post URL here to increase your post like ❤️‍🔥",
            )

            telegram_user.send_text_message(
                message=f"<i>Note: Make sure that your Instagram account is not private.</i>",
            )
        elif user_message.startswith("/me"):
            table = [
                [
                    "Name",
                    ":",
                    f"{telegram_user.user.first_name} {telegram_user.user.last_name}",
                ],
                ["ID", ":", telegram_user.user.username],
            ]
            msg = tabulate(table, tablefmt="plain")
            telegram_user.send_text_message(
                message=f"<pre>{msg}</pre>",
            )
        elif (
            user_message.startswith("https://www.instagram.com/p/")
            or user_message.startswith("https://www.instagram.com/reel/")
            or user_message.startswith("https://www.instagram.com/tv/")
        ):
            if not telegram_user.can_send_like:
                telegram_user.send_text_message(telegram_user.get_waiting_time)
                telegram_user.send_text_message(
                    'Follow my IG : <a href="https://instagram.com/arter_tendean">arter_tendean</a> 😉'
                )
                return Response()
            else:
                like_status = send_like(user_message)

                if like_status:
                    InstagramPost(user=telegram_user, url=user_message).save()
                    telegram_user.send_text_message(message=f"Success 😁👍")

                    # don't forget to update telegram user last send like date if like successfully sent
                    telegram_user.last_send_like_date = timezone.localtime()
                    telegram_user.save()
                else:
                    telegram_user.send_text_message(
                        message=f"Failed (┬┬﹏┬┬)",
                    )
                    telegram_user.send_text_message(
                        message=f"Try again later 😁👍",
                    )
                    return Response()
        else:
            telegram_user.send_text_message(
                'Follow my IG : <a href="https://instagram.com/arter_tendean">arter_tendean</a> 😉'
            )
            return Response()

        return HttpResponse(".")
