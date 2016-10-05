from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from models import Log

def helloView(request):
	logMessage("Message")
	result = ""
	for l in Log.objects.all():
		result += str(l) + "<br>"
	
	return HttpResponse(result)
	# return HttpResponse("Hello World!")


def logMessage(message):
	Log(description=message, reported=False).save()
	return
