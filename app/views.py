from django.http import HttpResponse
from django.shortcuts import redirect


def ping(request):
    return HttpResponse("Pong!")


def index(request):
    return redirect("https://github.com/animemoeus/telegram-bot", permanent=False)
