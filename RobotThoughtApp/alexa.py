from __future__ import absolute_import
from django_alexa.api import fields, intent, ResponseBuilder

# from models import Log
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
    continue
    """
    result = ""
    for l in Log.objects.all():
        if not l.reported:
            result += l.description + " . "
            l.reported = True
            l.save()

    if result == "":
        result = "Nothing at the moment. Please check back later."

    # TODO Spawn thread for StartStream()
    
    # return ResponseBuilder.create_response(message="Hello World 2!")
    return ResponseBuilder.create_response(message=result,
                                            reprompt="Would you like me to continue or quit?",
                                            end_session=False)
                                            # directives="AudioPlayer.Play",
                                            # audio_item = {"token": "explanation-audio", "url": "127.0.0.1:5005"})


def StartStream():
    import pyaudio
    import sys
    import numpy
    import socket

    UDP_IP = "0.0.0.0"
    UDP_PORT = 5005
    CHUNK = 1024

    # instantiate PyAudio (1)
    p = pyaudio.PyAudio()
    data = numpy.random.randint(0, 256, 44100 * 1000 * 10)

    # open stream (2)
    stream = p.open(format=p.get_format_from_width(2),
                    channels=1,
                    rate=44100,
                    output=True)

    # play stream (3)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    i = 0
    while i < data.size:
        chunk = data[i*CHUNK:(i+1)*CHUNK]
        chunk = ''.join([chr(j) for j in chunk])
        # stream.write(chunk)
        sock.sendto(chunk, (UDP_IP, UDP_PORT))
        i += CHUNK

    # stop stream (4)
    stream.stop_stream()
    stream.close()
    sock.close()

    # close PyAudio (5)
    p.terminate()
