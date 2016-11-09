from __future__ import absolute_import
from django_alexa.api import fields, intent, ResponseBuilder
from django.conf import settings
import pyttsx as tts
import threading
import pyaudio
import wave
import os
from subprocess import call

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
    end stream
    end audio
    end audio stream
    close stream
    close audio
    close audio stream
    """
    title, content = processAudio()
    return ResponseBuilder.create_response(end_session=False,
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
    return ResponseBuilder.create_response(end_session=False,
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
        title = "Stopping Audio Stream"
        content = "Stopping the Bluetooth audio stream."
    else:
        title = "Results Mode"
        content = "Reporting the results so far."
    
    engine = tts.init()
    engine.setProperty('rate', 150)
    engine.setProperty('voice', 'english-us')
    engine.startLoop(False)

    message = "Testing results mode." # TODO
    engine.say(message)
    engine.iterate()

    engine.endLoop()
    engine.stop()

    return ResponseBuilder.create_response(end_session=False,
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




class AudioThread(threading.Thread):
    def __init__(self, play_music=True):
        super(AudioThread, self).__init__()
        self._stop_event = threading.Event()
        self.play_music = play_music

        if self.play_music:
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
            if len(logs) == 0 and self.play_music:
                data = self.wf.readframes(self.CHUNK)
                if len(data) == 0:
                    self.wf.rewind()
                    data = self.wf.readframes(self.CHUNK)
                self.stream.write(data)
            else:
                log = logs.latest('id')
                message = log.description
                # call(["say", "-r", "200", "-v", "Fred", str(message)])
                self.engine.say(message)
                # _ = self.engine.runAndWait()
                self.engine.iterate()
                Log.objects.filter(reported=False).update(reported=True)
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
