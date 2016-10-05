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
    """
    result = ""
    for l in Log.objects.all():
        if not l.reported:
            result += l.description + " . "
            l.reported = True
            l.save()
    
    # return ResponseBuilder.create_response(message="Hello World 2!")
    return ResponseBuilder.create_response(message=result)
