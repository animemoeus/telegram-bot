from django.http import HttpResponse
from this import d


def ping(request):
    return HttpResponse("Pong!")
