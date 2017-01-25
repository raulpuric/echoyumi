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


messages = [
	"I'm initializing the Python interface to the ABB Robot arms",
	"I'm loading 3D object models",
	"I'm initializing the Kinect camera",
	"I'm loading the robust grasp set computed by Dex-Net",
	"I'm loading the object pose classifier Deep Learning network parameters",
	"My camera image suggests there are parts in the tray with confidence 78%",
	"I'm attempting to singulate parts with the paddle and right arm",
	"I've detected that {name of object} is singulated with confidence 88%",
	"I'm using the DL network to estimate the 3D stable pose of the yellow block",
	"I've determined the green block is in pose 3 with confidence 96%",
    "I can't reliably determine the pose of the white block",
    "I'm pushing [name of object] and hope that will make it easier to find it's pose",
	"I'm searching for the most robust, reachable grasp for the orange block in pose 3",
	"I'm moving the left arm and gripper into position",
	"I'm computing a collision free path to place the purple block into the box",
	"I detect the grasp was successful and the yellow block is now packed into the box",
	"I detect that this grasp failed",
	"I'm searching for an alternate robust, reachable grasp for the black block in pose 3. I'm now moving the gripper into position",
	"I don't detect any objects in the tray",
	"I detect that the left robot arm has accidentally collided with an object and must be reset",
	"I detect that the right robot arm has reached a joint limit/singularity and must be reset"
]

i = 0

def helloView(request):
	global i
	# logMessage(messages[i])
	i += 1
	i %= len(messages)
	
	result = ""
	last_1000 = Log.objects.order_by('-id')[:1000]
	for l in last_1000:
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
		self.CHUNK_SIZE = 1056 # 1024
		self.SLEEP_TIME = 1.0 * self.CHUNK_SIZE * 8 / 32e3 # 1024 bytes * (8 bits / byte) / (32,000 bits / sec)

		self.file_wrapper = None
		
		file_path = os.path.join(settings.STATIC_ROOT, 'song.mp3')
		self.music_file = open(file_path, 'r')

		# tts = gTTS(text="This is some background music.", lang='en')
		# self.music_file = TemporaryFile()
		# tts.write_to_fp(self.music_file)
		# self.music_file.seek(0)
		
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
