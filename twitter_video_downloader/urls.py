from django.urls import path

from .views import TelegramUserWebhook, download_video

urlpatterns = [
    path("telegram-webhook/", TelegramUserWebhook.as_view()),
    path("download-video/<slug:slug>/", download_video, name="download_video"),
]
