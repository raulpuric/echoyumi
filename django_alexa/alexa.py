from __future__ import absolute_import
from .api import intent, ResponseBuilder


@intent
def LaunchRequest(session):
    """
    Default Start Session Intent
    ---
    launch
    open
    resume
    start
    run
    load
    begin
    """
    return ResponseBuilder.create_response(message="Welcome.",
                                           reprompt="What would you like to do next?",
                                           end_session=False)


@intent
def CancelIntent(session):
    """
    Default Cancel Intent
    ---
    cancel
    """
    return ResponseBuilder.create_response(message="Canceling actions not configured!",
                                           reprompt="What would you like to do next?",
                                           end_session=False)


@intent
def StopIntent(session):
    """
    Default Stop Intent
    ---
    stop
    end
    nevermind
    """
    return ResponseBuilder.create_response(message="Stopping actions not configured!")

@intent
def PauseIntent(session):
    """
    Default Pause Intent
    ---
    pause
    wait
    """
    return ResponseBuilder.create_response(message="Pausing actions not configured!")


@intent
def HelpIntent(session):
    """
    Default Help Intent
    ---
    help
    info
    information
    """
    return ResponseBuilder.create_response(message="No help was configured!")


@intent
def SessionEndedRequest(session):
    """
    Default End Session Intent
    ---
    quit
    """
    return ResponseBuilder.create_response()

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
    return ResponseBuilder.create_response(message="Hello World 2!")