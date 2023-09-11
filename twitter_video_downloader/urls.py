from django.urls import path

from .views import TelegramUserWebhook

urlpatterns = [
    path("telegram-webhook/", TelegramUserWebhook.as_view()),
]
