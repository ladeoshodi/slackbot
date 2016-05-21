import time
import config
from slackclient import SlackClient

token = config.SLACKTOKEN
sc = SlackClient(token)

if sc.rtm_connect():
    while True:
        new_evts = sc.rtm_read()
        for evt in new_evts:
            print(evt)
            if "type" in evt:
                if evt["type"] == "message" and "text" in evt:
                    message = evt["text"]
            time.sleep(3)
else:
    print "Connection Failed, invalid token?"
