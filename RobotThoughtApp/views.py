from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def helloView(request):
    return HttpResponse("Hello World!")
