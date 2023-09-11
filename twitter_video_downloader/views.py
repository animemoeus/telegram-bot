import re

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .models import TelegramUser, Tweet
from .utils import ParseTelegramWebhook, get_video


class TelegramUserWebhook(GenericAPIView):
    def post(self, request):
        webhook = ParseTelegramWebhook(request.body)

        # We need to return a 200 OK HTTP status code, otherwise, the telegram server will spam the endpoint
        if not webhook.get_data():
            return Response(status=status.HTTP_200_OK)

        webhook = webhook.get_data()

        try:
            telegram_user = TelegramUser.objects.get(
                user_id=webhook.get("user").get("id")
            )
        except TelegramUser.DoesNotExist:
            telegram_user = TelegramUser.objects.create(
                user_id=webhook.get("user").get("id"),
                first_name=webhook.get("user").get("first_name"),
                last_name=webhook.get("user").get("last_name") or "",
                username=webhook.get("user").get("username") or "",
            )

        # Check if there is tweet valid ID in user message
        try:
            tweet_id = re.findall(r"[0-9]{15,100}", webhook.get("text_message"))[-1]
        except:
            tweet_id = None

        # Increase counter
        telegram_user.request_count += 1
        telegram_user.save()

        # Handle user message
        if webhook.get("text_message") == "/start":
            telegram_user.send_text_message(
                f"Hello {telegram_user.first_name} 😁\n\nSend the tweet link to me, and I will send the video download link for you."
            )
            return Response(status=status.HTTP_200_OK)

        if not tweet_id:
            telegram_user.send_text_message(f"Can't find tweet id from your message.")
            return Response(status=status.HTTP_200_OK)

        tweet_data = get_video(tweet_id)
        if not tweet_data.get("success"):
            telegram_user.send_text_message(tweet_data.get("message"))
        else:
            tweet = Tweet.objects.create(
                send_to=telegram_user.user_id, data=tweet_data.get("data")
            )
            telegram_user.send_text_message_inline_keyboard(
                message="💡 Ads keep us free for you.",
                inline_text="Download video now! ⚡",
                inline_url=f'https://telegram-bot.animemoe.us/{reverse("twitter_video_downloader:download_video", kwargs={"slug": tweet.id})}',
            )

        return Response(status=status.HTTP_200_OK)


@csrf_exempt
def download_video(request, slug=None):
    tweet = get_object_or_404(Tweet, id=slug)
    reverse("twitter_video_downloader:download_video", kwargs={"slug": tweet.id})

    if request.method == "GET":
        return render(
            request, "twitter_video_downloader/download.html", {"uuid": tweet.id}
        )

    if request.method == "POST":
        tweet.send_video_to_user()
        return HttpResponse(".")
