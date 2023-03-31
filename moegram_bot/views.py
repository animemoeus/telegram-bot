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

from app.serializers import TelegramUserSerializer

from .models import InstagramPost, TelegramUser
from .utils import get_or_create_telegram_user, send_like


def index(request):
    return HttpResponse("Hello, world")


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
            return Response({"detail": "This user is already blocked."})

        user_message = request.data.get("message", {}).get("text")
        if not user_message:
            telegram_user.send_text_message("Can't process this message.")
            return Response({"detail": "Can't process this message."})

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
                return Response({"detail": "Please wait before sending next like."})
            else:
                like_status = send_like(user_message)

                if like_status:
                    InstagramPost(user=telegram_user, url=user_message).save()
                    telegram_user.send_text_message(message=f"Success 😁👍")

                    # don't forget to update telegram user last send like date if like successfully sent
                    telegram_user.send_like_datetime = timezone.localtime()
                    telegram_user.save()
                    return Response({"detail": "Success to send like."})
                else:
                    telegram_user.send_text_message(
                        message=f"Failed (┬┬﹏┬┬)",
                    )
                    telegram_user.send_text_message(
                        message=f"Try again later 😁👍",
                    )
                    return Response({"detail": "Failed to send like."})
        else:
            telegram_user.send_text_message(
                'Follow my IG : <a href="https://instagram.com/arter_tendean">arter_tendean</a> 😉'
            )
            return Response({"detail": user_message})

        return HttpResponse(".")
