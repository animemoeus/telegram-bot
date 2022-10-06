from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("telegram-webhook/", views.telegram_webhook),
]
