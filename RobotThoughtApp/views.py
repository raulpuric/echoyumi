import numpy
from gtts import gTTS
from tempfile import TemporaryFile
from django.http import HttpResponse, StreamingHttpResponse
from wsgiref.util import FileWrapper

# Create your views here.
from models import Log



def helloView(request):
	# logMessage("Message")
	result = ""
	for l in Log.objects.all():
		result += str(l) + "<br>"
	
	return HttpResponse(result)

def logMessage(message):
	Log(description=message, reported=False).save()
	return







def streamAudioView(request):
	response = StreamingHttpResponse(
		streaming_content=AudioIterator(),
		content_type="audio/mpeg"
	)
	response['Content-Disposition'] = "attachment; filename=%s" % 'audio.mp3'

	return response

class AudioIterator:
	def __init__(self):
		self.time = 0
		self.file_wrapper = None
		return

	def __iter__(self):
		return self

	def next(self):
		if self.file_wrapper:
			try:
				# add a sleep delay here?
				return self.file_wrapper.next()
			except StopIteration, e:
				self.file_wrapper.close()
				self.file = None
				self.file_wrapper = None
				if self.time > 4:
					raise StopIteration
				else:
					return self.next()
		else:
			# message = 'Hello world '+str(self.time)+'!'
			logs = Log.objects.filter(reported=False)
			if len(logs) == 0:
				message = "Nothing at the moment. Please check back later."
				# eventually, replace this mesage with music
			else:
				# replace .first() with scheduling scheme?
				log = logs.first()
				log.reported = True
				log.save()
				message = log.description
			tts = gTTS(text=message, lang='en')
			self.file = TemporaryFile()
			tts.write_to_fp(self.file)
			self.file.seek(0)
			self.time += 1
			self.file_wrapper = FileWrapper(self.file, 1024)
			return self.next()
