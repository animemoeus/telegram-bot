from django.urls import path

from . import views

urlpatterns = [
    path("", views.Arter.as_view()),
]
