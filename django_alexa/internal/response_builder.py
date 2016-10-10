from __future__ import absolute_import
import logging

log = logging.getLogger(__name__)


class ResponseBuilder(object):
    """
    Simple class to help users to build alexa response data
    """
    version = ""

    @classmethod
    def set_version(cls, version):
        cls.version = version

    @classmethod
    def create_response(cls,
                        message=None, message_is_ssml=False,
                        reprompt=None, reprompt_is_ssml=False, reprompt_append=True,
                        title=None, content=None, card_type=None,
                        end_session=True, play_behavior = None, 
                        directives = None, audio_item = None, **kwargs):
        """
        Shortcut to create the data structure for an alexa response

        Output Speech:
        message - text message to be spoken out by the Echo
        message_is_ssml - If true the "message" is ssml formated and should be treated as such

        Reprompt Speech:
        reprompt - text message to be spoken out by the Echo
        reprompt_is_ssml - If true the "reprompt" is ssml formated and should be treated as such
        reprompt_append - If true the "reprompt" is append to the end of "message" for best practice voice interface design

        Card:
        card_type - A string describing the type of card to render. ("Simple", "LinkAccount")
        title - A string containing the title of the card. (not applicable for cards of type LinkAccount).
        content - A string containing the contents of the card (not applicable for cards of type LinkAccount).
                  Note that you can include line breaks in the content for a card of type Simple.

        end_session - flag to determine whether this interaction should end the session

        play_behavior - REPLACE_ALL (immediately play song, replace current and enqueued streams)
            - REPLACE_ENQUEUED (replace all enqueued streams, but keep playing current song)
            - ENQUEUE (add to end of queue)

        kwargs - Anything added here will be persisted across requests if end_session is False

        For more comprehensive documentation see:
        https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/alexa-skills-kit-interface-reference
        """
        data = {}
        data['version'] = cls.version
        data['response'] = cls._create_response(message, message_is_ssml,
                                               reprompt, reprompt_is_ssml, reprompt_append,
                                               title, content, card_type,
                                               end_session, play_behavior,
                                               directives, audio_item)
        data['sessionAttributes'] = kwargs
        log.debug("Response Data: {0}".format(data))
        print("Response Data: {0}".format(data))
        return data

    @classmethod
    def _create_response(cls,
                        message=None, message_is_ssml=False,
                        reprompt=None, reprompt_is_ssml=False, reprompt_append=True,
                        title=None, content=None, card_type=None,
                        end_session=True, play_behavior = None, 
                        directives = None, audio_item = None):
        data = {}
        data['shouldEndSession'] = end_session or (audio_item is not None)
        if message:
            if reprompt_append and reprompt is not None:
                message += " " + reprompt
                message_is_ssml = True if any([message_is_ssml, reprompt_is_ssml]) else False
            data['outputSpeech'] = cls._create_speech(message=message,
                                                      is_ssml=message_is_ssml)
        if title or content:
            data['card'] = cls._create_card(title=title,
                                            content=content,
                                            card_type=card_type)
        if reprompt:
            data['reprompt'] = cls._create_reprompt(message=reprompt,
                                                    is_ssml=reprompt_is_ssml)
        if directives:
            data['directives'] = cls._create_directives(directive_type = directives,
                                                        play_behavior = play_behavior,
                                                        audio_item = audio_item)
        return data

    @classmethod
    def _create_speech(cls, message=None, is_ssml=False):
        data = {}
        if is_ssml:
            data['type'] = "SSML"
            data['ssml'] = "<speak>" + message + "</speak>"
        else:
            data['type'] = "PlainText"
            data['text'] = message
        return data

    @classmethod
    def _create_reprompt(cls, message=None, is_ssml=False):
        data = {}
        data['outputSpeech'] = cls._create_speech(message=message,
                                                 is_ssml=is_ssml)
        return data

    @classmethod
    def _create_card(cls, title=None, content=None, card_type=None):
        data = {"type": card_type or "Simple"}
        if title: data["title"] = title
        if content: data["content"] = content
        return data

    @classmethod
    def _create_directives(cls, directive_type = "AudioPlayer.Play", play_behavior = "ENQUEUE",
        audio_item = None):
        data = {"type": directive_type, "playBehavior": play_behavior}
        if audio_item: data["audioItem"] = audio_item
        return data

    @classmethod
    def create_stream(cls, token = None, url = None, offsetInMilliseconds = 0,
                        **kwargs):
        """
        Shortcut to create the data structure for a stream in an Alexa Response's AudioItem

        token - name of the stream resource
        url - a publicly accessible url from where to stream/access your audio file
        offsetInMilliseconds - how much to delay the initial start of streaming
        """
        data = {}
        if token: data["token"] = token
        if url: data["url"] = url
        data["offsetInMilliseconds"] = offsetInMilliseconds

        return {'stream': data}
