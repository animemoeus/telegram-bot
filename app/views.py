from this import d
from django.http import HttpResponse


def ping(request):
    return HttpResponse("Pong!")
