from __future__ import absolute_import
from django_alexa.api import fields, intent, ResponseBuilder

from models import Log


@intent
def GetRobotThought(session, key):
    """
    Default GetRobotThought Intent
    ---
    what is my robot doing {key}
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
    
    # return ResponseBuilder.create_response(message="Hello World 2!")
    return ResponseBuilder.create_response(message=result)
