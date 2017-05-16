"""
The more general function declarations were used from the sample python Alexa
code provided by Amazon with some alterations made to them.
"""

from __future__ import print_function


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {"in_cpr":False, "compressions":False, "rescue_breaths":False}
    card_title = "Welcome"
    speech_output = "First Aid here, " + \
                    "What can I help you with? "
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me what you need help with by saying, " + \
                    "I need help with blank."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Hope I was able to help. "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def help_injured(intent, session):
    card_title = intent['name']
    session_attributes = {"in_cpr":False, "compressions":False, "rescue_breaths":False}
    should_end_session = False

    speech_output = "Call 911. "
    reprompt_text = None
    return build_response(session_attributes, build_speechlet_response(
      card_title, speech_output, reprompt_text, should_end_session))
      
      
def help_choking(intent, session):
    card_title = intent['name']
    session_attributes = {"in_cpr":False, "compressions":False, "rescue_breaths":False}
    should_end_session = False

    speech_output = "Is the person conscious or unconscious? "
    reprompt_text = None
    return build_response(session_attributes, build_speechlet_response(
      card_title, speech_output, reprompt_text, should_end_session))
      
      
def help_choking_conscious(intent, session):
    card_title = intent['name']
    session_attributes = {"in_cpr":False, "compressions":False, "rescue_breaths":False}
    should_end_session = False

    speech_output = "Call 911. "
    reprompt_text = None
    return build_response(session_attributes, build_speechlet_response(
      card_title, speech_output, reprompt_text, should_end_session))
    
    
def help_choking_unconscious(intent, session):
    card_title = intent['name']
    session_attributes = {"in_cpr":False, "compressions":False, "rescue_breaths":False}
    should_end_session = False

    speech_output = "Call 911. "
    reprompt_text = None
    return build_response(session_attributes, build_speechlet_response(
      card_title, speech_output, reprompt_text, should_end_session))
    
    
def help_cpr(intent, session):
    card_title = intent['name']
    session_attributes = {"in_cpr":True, "compressions":False, "rescue_breaths":False}
    should_end_session = False

    speech_output = "Lay the person on a firm, flat surface, you will give 30 chest compressions. " + \
                    "To give chest compressions push hard and fast in the middle of the chest about 2 inches down, " + \
                    "try to go at a rate of about 100 compressions per minute. " + \
                    "When you have given 30 compressions say done. When you are ready to begin say ready. "
    reprompt_text = None
    return build_response(session_attributes, build_speechlet_response(
      card_title, speech_output, reprompt_text, should_end_session))
      

def received_ready(intent, session):
    card_title = intent['name']
    session_attributes = {"in_cpr":True, "compressions":True, "rescue_breaths":False, "breath_intructions":True}
    should_end_session = False

    speech_output = "Begin giving chest compressions now, remember to go fast and say done when finished. "
    reprompt_text = None
    response = build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    response["response"]["outputSpeech"]["type"] = "SSML"
    del response["response"]["outputSpeech"]["text"]
    response["response"]["outputSpeech"]["ssml"] = "<speak> Try to give a compression every time I say one, I will count off thirty for you, " + \
                                                  "one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/>" + \
                                                  "one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/>" + \
                                                  "one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/>" + \
                                                  "one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/>" + \
                                                  "one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/>" + \
                                                  "one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/>," + \
                                                  "If you have completed the compressions say done </speak>"
    return response
    
    
def received_done(intent, session):
    card_title = intent['name']
    should_end_session = False

    if session.get('attributes', {})["compressions"]:
        session_attributes = {"in_cpr":True, "compressions":False, "rescue_breaths":True}
        if "breath_intructions" in session.get('attributes', {}):
            speech_output = "Now provide 2 rescue breaths, to do this tilt the head back and lift the chin up, " + \
                            "then pinch the nose and make a complete seal over the persons mouth, " + \
                            "blow in for 1 second to make the chest clearly rise, if the chest does not rise retilt the head and go again. " + \
                            "Do the 2 rescue breaths in quick succession and say done when finished. "
        else:
            speech_output = "Now provide 2 rescue breaths, say done when finished. "
        reprompt_text = None
        return build_response(session_attributes, build_speechlet_response(
          card_title, speech_output, reprompt_text, should_end_session))
    else:
        session_attributes = {"in_cpr":True, "compressions":True, "rescue_breaths":False}
        speech_output = "Now give 30 more chest compressions, say done when finished. "
        reprompt_text = None
        response = build_response(session_attributes, build_speechlet_response(
          card_title, speech_output, reprompt_text, should_end_session))
        response["response"]["outputSpeech"]["type"] = "SSML"
        del response["response"]["outputSpeech"]["text"]
        response["response"]["outputSpeech"]["ssml"] = "<speak> I will count off thirty for you," + \
                                                  "one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/>" + \
                                                  "one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/>" + \
                                                  "one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/>" + \
                                                  "one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/>" + \
                                                  "one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/>" + \
                                                  "one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/>," + \
                                                  "If you have completed the compressions say done </speak>"
        return response
    
    
def help_aed(intent, session):
    card_title = intent['name']
    session_attributes = {"in_cpr":False, "compressions":False, "rescue_breaths":False}
    should_end_session = False

    speech_output = "Call 911. "
    reprompt_text = None
    return build_response(session_attributes, build_speechlet_response(
      card_title, speech_output, reprompt_text, should_end_session))
      
      
def help_bleeding(intent, session):
    card_title = intent['name']
    session_attributes = {"in_cpr":False, "compressions":False, "rescue_breaths":False}
    should_end_session = False

    speech_output = "Call 911. "
    reprompt_text = None
    return build_response(session_attributes, build_speechlet_response(
      card_title, speech_output, reprompt_text, should_end_session))
      

def help_burns(intent, session):
    card_title = intent['name']
    session_attributes = {"in_cpr":False, "compressions":False, "rescue_breaths":False}
    should_end_session = False

    speech_output = "Call 911. "
    reprompt_text = None
    return build_response(session_attributes, build_speechlet_response(
      card_title, speech_output, reprompt_text, should_end_session))
      
      
def help_poisoning(intent, session):
    card_title = intent['name']
    session_attributes = {"in_cpr":False, "compressions":False, "rescue_breaths":False}
    should_end_session = False

    speech_output = "Call 911. "
    reprompt_text = None
    return build_response(session_attributes, build_speechlet_response(
      card_title, speech_output, reprompt_text, should_end_session))
      
      
def help_neck(intent, session):
    card_title = intent['name']
    session_attributes = {"in_cpr":False, "compressions":False, "rescue_breaths":False}
    should_end_session = False

    speech_output = "Call 911. "
    reprompt_text = None
    return build_response(session_attributes, build_speechlet_response(
      card_title, speech_output, reprompt_text, should_end_session))
      
      
def help_spinal(intent, session):
    card_title = intent['name']
    session_attributes = {"in_cpr":False, "compressions":False, "rescue_breaths":False}
    should_end_session = False

    speech_output = "Call 911. "
    reprompt_text = None
    return build_response(session_attributes, build_speechlet_response(
      card_title, speech_output, reprompt_text, should_end_session))
      
      
def help_stroke(intent, session):
    card_title = intent['name']
    session_attributes = {"in_cpr":False, "compressions":False, "rescue_breaths":False}
    should_end_session = False

    speech_output = "Call 911. "
    reprompt_text = None
    return build_response(session_attributes, build_speechlet_response(
      card_title, speech_output, reprompt_text, should_end_session))
      
     
def how_do_i_do(intent, session):
    card_title = intent['name']
    session_attributes = {"in_cpr":session.get('attributes', {})["in_cpr"], "compressions":False, "rescue_breaths":False}
    should_end_session = False
    
    if 'Step' in intent['slots']:
        if intent['slots']['Step']['value'] == "chest compressions":
            speech_output = "Lay the person on a firm, flat surface and push hard and fast in the middle of their chest about 2 inches down. " + \
                            "Do this 30 times then switch to rescue breaths, try to push at a rate of 100 per minute. "
            reprompt_text = None
            return build_response(session_attributes, build_speechlet_response(
                card_title, speech_output, reprompt_text, should_end_session))
        else:
            speech_output = "Tilt the head back and lift the chin up, then pinch the nose and make a complete seal over the persons mouth, " + \
                            "blow in for 1 second to make the chest clearly rise, if the chest does not rise retilt the head and go again. " + \
                            "Do the 2 rescue breaths in quick succession. "
            reprompt_text = None
            return build_response(session_attributes, build_speechlet_response(
                card_title, speech_output, reprompt_text, should_end_session))
    else:
        speech_output = "I'm sorry I didn't understand what you asked. "
        reprompt_text = None
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))
            
    
def restart_cpr(intent, session):
    card_title = intent['name']
    should_end_session = False
    
    if 'Step' in intent['slots']:
        if intent['slots']['Step']['value'] == "chest compressions":
            session_attributes = {"in_cpr":True, "compressions":True, "rescue_breaths":False}
            speech_output = "Beginning chest compressions, remember to give 30 and to go fast. " + \
                            "When you are done say done. "
            reprompt_text = None
            response = build_response(session_attributes, build_speechlet_response(
              card_title, speech_output, reprompt_text, should_end_session))
            response["response"]["outputSpeech"]["type"] = "SSML"
            del response["response"]["outputSpeech"]["text"]
            response["response"]["outputSpeech"]["ssml"] = "<speak> I will count off thirty for you," + \
                                                  "one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/>" + \
                                                  "one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/>" + \
                                                  "one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/>" + \
                                                  "one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/>" + \
                                                  "one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/>" + \
                                                  "one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/> one <break time='60ms'/>," + \
                                                  "If you have completed the compressions say done </speak>"
            return response
        else:
            session_attributes = {"in_cpr":True, "compressions":False, "rescue_breaths":True}
            speech_output = "Begin giving the 2 rescue breaths, when you are finished say done. "
            reprompt_text = None
            return build_response(session_attributes, build_speechlet_response(
              card_title, speech_output, reprompt_text, should_end_session))
    else:
        session_attributes = {"in_cpr":False, "compressions":False, "rescue_breaths":False}
        speech_output = "I'm sorry, which step did you want to restart? "
        reprompt_text = None
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))
    
    
def check_quit_cpr(intent, session):
    card_title = intent['name']
    session_attributes = {"in_cpr":True, "compressions":session.get('attributes', {})["compressions"], "rescue_breaths":session.get('attributes', {})["rescue_breaths"], "quitting_cpr":True}
    should_end_session = False
    
    speech_output = "Are you sure you want to stop giving CPR? "
    reprompt_text = None
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
     

def quit_cpr(intent, session):
    card_title = intent['name']
    session_attributes = {"in_cpr":False, "compressions":False, "rescue_breaths":False}
    should_end_session = False
    
    speech_output = "Ok, no longer giving instructions for CPR. "
    reprompt_text = None
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    
    
def what_can_i_do(intent, session):
    card_title = intent['name']
    session_attributes = {"in_cpr":session.get('attributes', {})["in_cpr"], "compressions":session.get('attributes', {})["compressions"], "rescue_breaths":session.get('attributes', {})["rescue_breaths"]}
    should_end_session = False
    
    if session.get('attributes', {}) and "in_cpr" in session.get('attributes', {}) and session.get('attributes', {})["in_cpr"]:
        speech_output = "You can ask: how do i do chest compressions or how do i do rescue breaths to hear the instructions again, " + \
                        "or restart chest compressions or restart rescue breaths to restart a step, " + \
                        "or stop CPR or quit CPR to stop providing CPR instructions. "
        reprompt_text = None
    else:
        speech_output = "I can help with: " + \
                            "checking an injured adult, " + \
                            "choking, " + \
                            "CPR, " + \
                            "AED, " + \
                            "controlling bleeding, " + \
                            "burns, " + \
                            "poisoning, " + \
                            "neck injuries, " + \
                            "spinal injuries, " + \
                            "and strokes. " + \
                            "To get help with one of these things say I need help with, followed by what you need help with. "
        reprompt_text = "Do you need help with any of these things? "
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "WhatCanIDoIntent":
        return what_can_i_do(intent, session)
    elif intent_name == "ConsciousChokingIntent":
        return help_choking_conscious(intent, session)
    elif intent_name == "UnconsciousChokingIntent":
        return help_choking_unconscious(intent, session)
    elif intent_name == "InjuredIntent":
        return help_injured(intent, session)
    elif intent_name == "ChokingIntent":
        return help_choking(intent, session)
    elif intent_name == "CPRIntent":
        return help_cpr(intent, session)
    elif intent_name == "AEDIntent":
        return help_aed(intent, session)
    elif intent_name == "BleedingIntent":
        return help_bleeding(intent, session)
    elif intent_name == "BurnIntent":
        return help_burns(intent, session)
    elif intent_name == "PoisonIntent":
        return help_poisoning(intent, session)
    elif intent_name == "NeckIntent":
        return help_neck(intent, session)
    elif intent_name == "SpinalIntent":
        return help_spinal(intent, session)
    elif intent_name == "StrokeIntent":
        return help_stroke(intent, session)
    elif intent_name == "ReadyIntent":
        return received_ready(intent, session)
    elif intent_name == "DoneIntent":
        return received_done(intent, session)
    elif intent_name == "HowDoIDoIntent":
        return how_do_i_do(intent, session)
    elif intent_name == "RestartIntent":
        return restart_cpr(intent, session)
    elif intent_name == "QuitCPRIntent":
        return check_quit_cpr(intent, session)
    elif intent_name == "AMAZON.YesIntent" and "quitting_cpr" in session.get('attributes', {}):
        return quit_cpr(intent, session)
    elif intent_name == "AMAZON.NoIntent" and "quitting_cpr" in session.get('attributes', {}):
        return received_done(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        return ValueError("Invalid Intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    if (event['session']['application']['applicationId'] !=
            "amzn1.ask.skill.9dedbbdf-97e5-4174-b0c2-4f1df37b3665"):
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
