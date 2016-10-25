from __future__ import absolute_import
from django_alexa.api import fields, intent, ResponseBuilder
from django.conf import settings
import pyttsx as tts
import threading
import pyaudio
import wave
import os

from RobotThoughtApp.models import Log


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
    """
    global audio_thread
    if audio_thread is not None:
        stop_bluetooth_thread()
        title = "Stopping Audio Stream"
        content = "Stopping the Bluetooth audio stream."
    else:
        start_bluetooth_thread()
        title = "Play Audio Stream"
        content = "Streaming the robot logs via Bluetooth."
    return ResponseBuilder.create_response(end_session=True, # should be true for audio streams
                                            title=title,
                                            content=content
                                          )
    # return ResponseBuilder.create_response(message="",
    #                                         reprompt="",
    #                                         end_session=True, # should be true for audio streams
    #                                         title="Play Audio Stream",
    #                                         content="Streaming the robot logs.",
    #                                         directives=[
    #                                             ResponseBuilder.create_stream_directive(
    #                                                 playBehavior="REPLACE_ALL",
    #                                                 token="explainable-audio",
    #                                                 url="https://134e60a0.ngrok.io/audio.mp3"
    #                                             )
    #                                         ]
    #                                     )



class AudioThread(threading.Thread):
    def __init__(self):
        super(AudioThread, self).__init__()
        self._stop_event = threading.Event()
        
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
        self.engine = tts.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('voice', 'english-us')
        self.engine.startLoop(False)
        return

    def stop(self):
        self._stop_event.set()
        return

    def stopped(self):
        return self._stop_event.isSet()

    def run(self):
        while not self.stopped():
            logs = Log.objects.filter(reported=False)
            if len(logs) == 0:
                data = self.wf.readframes(self.CHUNK)
                self.stream.write(data)
            else:
                log = logs.latest('id')
                message = log.description
                logs.update(reported=True)
                self.engine.say(message)
                # _ = self.engine.runAndWait()
                self.engine.iterate()
        self.engine.endLoop()
        self.engine.stop()
        self.stream.close()
        self.p.terminate()
        return


audio_thread = None

def start_bluetooth_thread():
    global audio_thread
    audio_thread = AudioThread()
    audio_thread.daemon = True
    audio_thread.start()
    return

def stop_bluetooth_thread():
    global audio_thread
    if audio_thread is not None:
        audio_thread.stop()
        audio_thread = None
    return
