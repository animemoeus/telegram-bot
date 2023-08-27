from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView

from app.utils import TelegramWebhookHandler


class Arter(APIView):
    def post(self, request):
        webhook = TelegramWebhookHandler(request.body)

        if not webhook.is_valid:
            return HttpResponse(
                "Invalid webhook request", status=status.HTTP_400_BAD_REQUEST
            )

        if webhook.is_valid:
            print(webhook.get_user_data())

        return HttpResponse("arter tendean")
