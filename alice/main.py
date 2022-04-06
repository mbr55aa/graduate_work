import phrases
from movies import get_director, get_actor
from phrases import get_phrase


def handler(event, context):
    current_state = event.get("state", {}).get("session", {}).get("current_state", {})
    last_phrase = event.get("state", {}).get("session", {}).get("last_phrase")
    intents = event.get("request", {}).get("nlu", {}).get("intents", {})
    command = event.get("request", {}).get("command")

    text = get_phrase(phrases.INTRO)
    end_session = "false"

    if intents.get("exit"):
        text = get_phrase(phrases.EXIT)
        end_session = "true"
    elif intents.get("help"):
        text = get_phrase(phrases.HELP)
    elif intents.get("repeat"):
        if last_phrase:
            text = last_phrase
        else:
            text = get_phrase(phrases.REPEAT)
    elif intents.get("director"):
        text, current_state = get_director(intents.get("director"), current_state)
    elif intents.get("actor"):
        text, current_state = get_actor(intents.get("actor"), current_state)
    elif command:
        text = get_phrase(phrases.UNSUCCESSFUL)

    response = {
        "version": event["version"],
        "session": event["session"],
        "response": {"text": text, "end_session": end_session},
        "session_state": {"current_state": current_state, "last_phrase": text},
    }

    return response
