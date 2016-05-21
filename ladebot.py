import config
from slackclient import SlackClient

token = config.SLACKTOKEN
sc = SlackClient(token)

# channel = "D1ANVTWTT"
text = "Hello\nNice to meet you"

# sending a personal message to myself

# get user list, slack api testing is okay for this
# my ID
user = "U0LD07GUX"

# open the IM channel and get the channel id
channel = sc.api_call("im.open", user=user)["channel"]["id"]

# send a message to me as ladebot
sc.api_call("chat.postMessage", channel=channel, text=text, as_user="true")

# send messages to the public and private test channels
sc.api_call("chat.postMessage", channel="#testing-private", text=text, as_user="true")
sc.api_call("chat.postMessage", channel="#testing-public", text=text, as_user="true")


# checkout history with ladebot
print sc.api_call("im.history", channel=channel)
