from __future__ import absolute_import, division
from django_alexa.api import fields, intent, ResponseBuilder
from django.conf import settings
from subprocess import call
from gtts import gTTS
import os, sys, time
import pyaudio, wave
import threading
import pyttsx

from RobotThoughtApp.models import Log



########################
##### Main Intents #####
########################

@intent
def GetRobotThought(session):
    """
    Default GetRobotThought Intent
    ---
    what is my robot doing
    tell me what my robot is doing
    how is my robot doing
    what is the robot doing
    what is the yumi robot doing
    what is yumi doing
    what's up
    how are you doing
    speak
    continue
    end stream
    end audio
    end audio stream
    close stream
    close audio
    close audio stream
    """
    title, content = processAudio()
    return ResponseBuilder.create_response(end_session=True,
                                            title=title,
                                            content=content
                                          )


@intent
def RunInDevMode(session):
    """
    Default RunInDevMode Intent
    ---
    run in dev mode
    run dev mode
    run dev
    dev mode
    dev
    """
    global audio_thread
    if audio_thread is not None:
        stop_bluetooth_thread()
    title, content = processAudio(play_music=False)
    return ResponseBuilder.create_response(end_session=True,
                                            title=title,
                                            content=content
                                          )


@intent
def RunInResultsMode(session):
    """
    Default RunInResultsMode Intent
    ---
    run in results mode
    tell me the results
    show me the results
    results
    """
    global audio_thread
    if audio_thread is not None:
        stop_bluetooth_thread()
        title = "Stopping Audio Stream, entering Results Mode"
        content = "Stopping the Bluetooth audio stream. Reporting the results so far."
    else:
        title = "Results Mode"
        content = "Reporting the results so far."

    message = "Testing results mode."
    # total = Log.objects.filter(description__icontains="singulat").count()
    # success = Log.objects.filter(Q(description__icontains="singulat") & ~Q(description__icontains="fail")).count()
    # if total == 0:
    #     success_rate = 0.0
    # else:
    #     success_rate = 100.0 * success / total

    # message = "%d percent success rate on singulation."

    return ResponseBuilder.create_response(message=message,
                                            end_session=True,
                                            title=title,
                                            content=content
                                          )




def processAudio(play_music=True):
    global audio_thread
    if audio_thread is not None:
        stop_bluetooth_thread()
        title = "Stopping Audio Stream"
        content = "Stopping the Bluetooth audio stream."
    else:
        start_bluetooth_thread(play_music)
        title = "Playing Audio Stream"
        content = "Streaming the robot logs via Bluetooth."
    return title, content




#############################
##### Main Audio Thread #####
#############################

class AudioThread(threading.Thread):
    def __init__(self, play_music=True):
        super(AudioThread, self).__init__()
        self._stop_event = threading.Event()
        self.play_music = play_music

        self.CHUNK = 1024
        file_path = os.path.join(settings.STATIC_ROOT, 'song.wav')
        self.wf = wave.open(file_path, 'rb')
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format = self.p.get_format_from_width(self.wf.getsampwidth()),
            channels = self.wf.getnchannels(),
            rate = self.wf.getframerate(),
            output = True
        )

        Log.objects.filter(reported=False).update(reported=True)
        self.engine = pyttsx.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('voice', 'english-us')
        self.engine.startLoop(False)
        return

    def stop(self):
        self._stop_event.set()
        return

    def stopped(self):
        return self._stop_event.isSet()

    def get_music(self, chunk_size):
        data = self.wf.readframes(chunk_size)
        if len(data) < chunk_size:
            self.wf.rewind()
            data += self.wf.readframes(chunk_size - len(data))
        return data

    def merge_audio(self, data1, weight1, data2, weight2):
        # http://stackoverflow.com/questions/4039158/mixing-two-audio-files-together-with-python
        def bin_to_int(bin):
            as_int = 0
            for char in bin[::-1]: # iterate over each char in reverse (because little-endian)
                as_int <<= 8
                as_int += ord(char)
            return as_int
        def int_to_bin(as_int):
            as_bin = ''
            while as_int > 0:
                as_bin += chr(as_int % 2**8)
                as_int >>= 8
            return as_bin

        samples1 = [data1[i:i+2] for i in xrange(0, len(data1), 2)]
        samples2 = [data2[i:i+2] for i in xrange(0, len(data2), 2)]

        samples1 = [bin_to_int(s) for s in samples1]
        samples2 = [bin_to_int(s) for s in samples2]

        samples_avg = [int((s1*weight1 + s2*weight2)/(weight1 + weight2)) for (s1, s2) in zip(samples1, samples2)]

        data = [int_to_bin(s) for s in samples_avg]
        data = ''.join(data)

        return data

    def play_message(self, message):
        file_path = os.path.join(settings.STATIC_ROOT, 'messages', message.lower().replace(" ", "_").replace('/', '_')+'.wav')
        if os.path.isfile(file_path):
            wf = wave.open(file_path, 'rb')
            msg_data = wf.readframes(sys.maxint)
            music_data = self.get_music(len(msg_data))
            # data = self.merge_audio(msg_data, 2.0, music_data, 1.0)
            data = msg_data
            self.stream.write(data)
        else:
            self.engine.say(message)
            self.engine.iterate()
            # spawn thread to convert message to wav file
            start_gtts_thread(message)
        return

    def run(self):
        while not self.stopped():
            logs = Log.objects.filter(reported=False)
            if len(logs) == 0 and not self.play_music:
                time.sleep(0.01)
            elif len(logs) == 0 and self.play_music:
                data = self.get_music(self.CHUNK)
                self.stream.write(data)
            else:
                log = logs.latest('id')
                message = log.description
                Log.objects.filter(reported=False).update(reported=True)
                self.play_message(message)
        self.engine.endLoop()
        self.engine.stop()
        self.stream.close()
        self.p.terminate()
        return



audio_thread = None

def start_bluetooth_thread(play_music=True):
    global audio_thread
    audio_thread = AudioThread(play_music)
    audio_thread.daemon = True
    audio_thread.start()
    return

def stop_bluetooth_thread():
    global audio_thread
    if audio_thread is not None:
        audio_thread.stop()
        audio_thread = None
    return




##################################
##### gTTS Conversion Thread #####
##################################

def gtts_to_wav(message):
    tts = gTTS(text=message, lang='en')
    file_name = message.lower().replace(" ", "_").replace('/', '_')
    file_path = os.path.join(settings.STATIC_ROOT, 'messages', file_name)
    tts.save(file_path + ".mp3")
    call(["ffmpeg", "-i", file_path + ".mp3",
        "-acodec", "pcm_s16le",
        "-ac", "1",
        "-ar", "24000",
        file_path + ".wav"])
    os.remove(file_path + ".mp3")
    return

def audify_database():
    database = [str(a['description']).lower().replace('/', ' ') for a in Log.objects.values('description')]
    database = set(database)
    saved = [a[:-4].replace('_', ' ') for a in os.listdir(os.path.join(settings.STATIC_ROOT, 'messages'))]
    saved = set(saved)
    
    messages = database - saved
    for message in messages:
        gtts_to_wav(message)
    return

def start_gtts_thread(message):
    gtts_thread = threading.Thread(target=gtts_to_wav, args=(message,))
    gtts_thread.daemon = True
    gtts_thread.start()
    return

audify_database()



############################
##### Grasping Intents #####
############################

COLORS = ("orange", "red", "white", "yellow", "gold", "black", "pink", "blue")

COLOR_TO_PART_NAME = {
    "orange": "bar_clamp",
    "red": "vase",
    "white": "part3",
    "yellow": "pawn",
    "gold": "part1",
    "black": "gearbox",
    "pink": "turbine_housing",
    "blue": "nozzle"
}


class GraspOneSlots(fields.AmazonSlots):
    paramOne = fields.AmazonCustom(label="LIST_OF_COLORS", choices=COLORS)

class GraspTwoSlots(GraspOneSlots):
    paramTwo = fields.AmazonCustom(label="LIST_OF_COLORS", choices=COLORS)

class GraspThreeSlots(GraspTwoSlots):
    paramThree = fields.AmazonCustom(label="LIST_OF_COLORS", choices=COLORS)

class GraspFourSlots(GraspThreeSlots):
    paramFour = fields.AmazonCustom(label="LIST_OF_COLORS", choices=COLORS)

class GraspFiveSlots(GraspFourSlots):
    paramFive = fields.AmazonCustom(label="LIST_OF_COLORS", choices=COLORS)

class GraspSixSlots(GraspFiveSlots):
    paramSix = fields.AmazonCustom(label="LIST_OF_COLORS", choices=COLORS)

class GraspSevenSlots(GraspSixSlots):
    paramSeven = fields.AmazonCustom(label="LIST_OF_COLORS", choices=COLORS)

class GraspEightSlots(GraspSevenSlots):
    paramEight = fields.AmazonCustom(label="LIST_OF_COLORS", choices=COLORS)


@intent(slots=GraspOneSlots)
def Grasp1(session, paramOne):
    return log_grasps(1, [paramOne])

@intent(slots=GraspTwoSlots)
def Grasp2(session, paramOne, paramTwo):
    return log_grasps(2, [paramOne, paramTwo])

@intent(slots=Grasp3Slots)
def Grasp3(session, paramOne, paramTwo, paramThree):
    return log_grasps(3, [paramOne, paramTwo, paramThree])

@intent(slots=Grasp4Slots)
def Grasp4(session, paramOne, paramTwo, paramThree, paramFour):
    return log_grasps(4, [paramOne, paramTwo, paramThree, paramFour])

@intent(slots=Grasp5Slots)
def Grasp5(session, paramOne, paramTwo, paramThree, paramFour, paramFive):
    return log_grasps(5, [paramOne, paramTwo, paramThree, paramFour, paramFive])

@intent(slots=Grasp6Slots)
def Grasp6(session, paramOne, paramTwo, paramThree, paramFour, paramFive, paramSix):
    return log_grasps(6, [paramOne, paramTwo, paramThree, paramFour, paramFive, paramSix])

@intent(slots=Grasp7Slots)
def Grasp7(session, paramOne, paramTwo, paramThree, paramFour, paramFive, paramSix, paramSeven):
    return log_grasps(7, [paramOne, paramTwo, paramThree, paramFour, paramFive, paramSix, paramSeven])

@intent(slots=Grasp8Slots)
def Grasp8(session, paramOne, paramTwo, paramThree, paramFour, paramFive, paramSix, paramSeven, paramEight):
    return log_grasps(8, [paramOne, paramTwo, paramThree, paramFour, paramFive, paramSix, paramSeven, paramEight])


@intent
def GraspAll(session):
    return log_grasps("all", ["all"])


def log_grasps(number, params):
    if params[0] == "all":
        parts = params
    else:
        parts = [COLOR_TO_PART_NAME[c] for c in params]
    line = ','.join(parts).lower()
    
    # Write to file
    f = open("/home/autolab/Workspace/rishi_working/echoyumi/grasp_command.txt", 'w')
    f.write(line)
    f.close()

    return ResponseBuilder.create_response(end_session=True,
            title="Grasp "+str(number),
            content="Grasping "+str(number)+" items"
        )

