from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .models import TelegramUser
from .utils import ParseTelegramWebhook


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

        telegram_user.request_count += 1
        telegram_user.save()

        return Response(status=status.HTTP_200_OK)
