import config
import requests
from slackclient import SlackClient

KEYWORD = "define"
MESSAGE_LENGTH = 2

token = config.SLACKTOKEN
sc = SlackClient(token)


# function to hit free api (wordnik.com) and return defined word
def define(word):
    api_key = config.WORDNIK_TOKEN
    limit = "1"
    includeRelated = "true"
    sourceDictionaries = "all"
    useCanonical = "true"
    url = (
        "http://api.wordnik.com:80/v4/word.json/{0}/definitions"
        "?limit={1}&includeRelated={2}&sourceDictionaries={3}"
        "&useCanonical={4}&api_key={5}"
    ).format(word, limit, includeRelated,
             sourceDictionaries, useCanonical, api_key)

    response = requests.get(url)
    try:
        response = response.json()
        return response[0]
    except:
        return None


# post the definition back to the channel
def post_message(definition, channel):
    # get text format to return
    if definition:
        defined_word = definition["text"]
        partOfSpeech = definition["partOfSpeech"]
        text = (
            "Definition: {0}\n"
            "Part of Speech: {1}\n"
        ).format(defined_word, partOfSpeech)
    else:
        text = "Sorry can't define this word"

    # post the message
    sc.api_call("chat.postMessage", channel=channel, text=text, as_user="true")


# a very long function accessing slack rtm and listening to events
if sc.rtm_connect():
    while True:
        new_evts = sc.rtm_read()
        for evt in new_evts:
            # check that the type is a message and has a text in it
            if evt.get("type") == "message" and "text" in evt:
                # get the message
                message = evt["text"]

                # split sentence to get what to define
                split_mssg = message.split(" ")

                # check if the first word matches keyword "define"
                if split_mssg[0] == KEYWORD and len(split_mssg) == MESSAGE_LENGTH:
                    # get the channel
                    channel = evt["channel"]

                    # get the word to define
                    word = " ".join(split_mssg[1:])
                    definition = define(word)
                    post_message(definition, channel)
else:
    print "Connection Failed, invalid token?"
