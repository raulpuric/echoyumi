from django_alexa.api import fields, intent, Slots, ResponseBuilder

@intent
def LaunchRequest(session):
    """
    Welcome to Yumi message
    ---
    launch
    start
    run
    begin
    open
    """
    return ResponseBuilder.create_response(message="Welcome to the Yumi custom skill!",
                                           reprompt="What would you like to ask the Yumi?",
                                           end_session=False,
                                           launched=True)
@intent
def AddPointsToHouse(session, arg1, arg2):
    """
    Direct response to add points to a house
    ---
    {arg1} {arg2}
    {arg1} and {arg2}
    testing {arg1} and {arg2}
    testing {arg1} testing {arg2}
    """
    kwargs = {}
    kwargs['message'] = "Received messages {0} and {1}.".format(arg1, arg2)
    if session.get('launched'):
        kwargs['reprompt'] = "What would you like to ask the Yumi?"
        kwargs['end_session'] = False
        kwargs['launched'] = session['launched']
    return ResponseBuilder.create_response(**kwargs)
