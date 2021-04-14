import os
from slack_bolt import App

class SlackBot:
    CHANNEL_ID = "C01U99F6BPW"
    app = App(
        token=os.environ.get("SLACK_BOT_TOKEN"),
        signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
    )

    response = app.client.conversations_members(channel=CHANNEL_ID)
    members = response["members"]
    users = []
    
    for member in members:
        response = (app.client.users_info(user=member))
        profile = response["user"]["profile"]
        display_name = profile["display_name"]
        users.append(display_name)
        print(member + ": " + display_name)
