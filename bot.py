import slack
import os
from pathlib import Path
from dotenv import load_dotenv

class SlackBot(object):
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path = env_path)

    client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

    response = client.users_list()
    users = response["members"]
    user_ids = list(map(lambda u: u["id"], users))


# client.chat_postMessage(channel="#test-bot", text="Hello World!")