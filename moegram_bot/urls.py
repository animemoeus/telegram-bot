from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("telegram-webhook/v1/", views.telegram_webhook_v1),
]
