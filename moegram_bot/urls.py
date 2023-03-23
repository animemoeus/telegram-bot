from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    # path("telegram-webhook/", views.telegram_webhook),
    path(
        "telegram-webhook-v2/",
        views.TelegramWebhookV2.as_view(),
        name="telegram-webhook-v2",
    ),
]
