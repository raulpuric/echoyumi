import logging, os, time
from gtts import gTTS
from django.conf import settings
from django.http import HttpResponse, StreamingHttpResponse
from django.contrib.staticfiles.templatetags.staticfiles import static
from tempfile import TemporaryFile
from wsgiref.util import FileWrapper


# Create your views here.
from models import Log

log = logging.getLogger(__name__)



def helloView(request):
	logMessage("Message")
	result = ""
	for l in Log.objects.all():
		result += str(l) + "<br>"

	log.debug("Homepage accessed")
	
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
		self.CHUNK_SIZE = 1024 * 8
		self.SLEEP_TIME = 1.0 * self.CHUNK_SIZE * 8 / 32e3 # 1024 bytes * (8 bits / byte) / (32,000 bits / sec)

		self.file_wrapper = None
		file_path = os.path.join(settings.STATIC_ROOT, 'song.mp3')
		self.music_file = open(file_path, 'r')
		self.music_file_wrapper = FileWrapper(self.music_file, self.CHUNK_SIZE)
		return

	def __iter__(self):
		return self

	def get_next_music(self):
		try:
			time.sleep( self.SLEEP_TIME )
			return self.music_file_wrapper.next()
		except StopIteration, e:
			self.music_file.seek(0)
			return self.get_next_music()
		# else, raise an error to stop the entire stream
		raise StopIteration

	def next(self):
		if self.file_wrapper is not None:
			try:
				time.sleep( self.SLEEP_TIME ) # in seconds
				return self.file_wrapper.next()
			except StopIteration, e:
				self.file_wrapper.close()
				self.file = None
				self.file_wrapper = None
				return self.next()
		else:
			logs = Log.objects.filter(reported=False)
			if len(logs) == 0:
				# message = "Nothing at the moment. Please check back later."
				return self.get_next_music()
			
			log = logs.latest('id')
			message = log.description
			logs.update(reported=True)

			tts = gTTS(text=message, lang='en')
			self.file = TemporaryFile()
			tts.write_to_fp(self.file)
			self.file.seek(0)
			self.file_wrapper = FileWrapper(self.file, self.CHUNK_SIZE)
			return self.next()
