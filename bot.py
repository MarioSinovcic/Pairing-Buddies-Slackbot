import os
import random
import boto3
from slack_bolt import App
from secrets_retriever import SecretsRetriever

SINGLE_USER = "You're the only pear on this tree. Best find more fruit friends to pear with!\n(The pearing bot has only found 1 human user in this channel, feel free to remove it if not in use)."
MESSAGE_HEADER = "You hear a rustling from the fruit bowl nearby. A lone pear within declares: \n\n"

class SlackBot:
    def __init__(self):
        client = boto3.client('ssm')

        self.slack_bot_token = client.get_parameter(
            Name='/mario/pairing-bot/SLACK_BOT_TOKEN',
            WithDecryption=True
        )['Parameter']['Value']

        self.slack_signing_secret = client.get_parameter(
            Name='/mario/pairing-bot/SLACK_SIGNING_SECRET',
            WithDecryption=True
        )['Parameter']['Value']

        self.CHANNEL_ID = "C01U99F6BPW"
        self.app = App(
            token=self.slack_bot_token,
            signing_secret=self.slack_signing_secret
        )

    def run(self):
        user_ids = self.get_user_ids() 
        print(user_ids)
        shuffled_ids = self.shuffle_user_ids(user_ids=user_ids)
        print("user ids shuffled")
        self.post_to_channel(user_ids=user_ids)

    def get_user_ids(self):
        response = self.app.client.conversations_members(channel=self.CHANNEL_ID)
        user_ids = response["members"]
        print("user ids gotten")
        
        for user_id in user_ids:
            response = self.app.client.users_info(user=user_id)
            is_bot = response["user"]["is_bot"]
            if is_bot:
                user_ids.remove(user_id)

        user_ids += ["Ashley", "Tom", "Lindsay", "Alvin", "Leah", "Taylor", "Chrisna", "Sam"]
        return user_ids

    def verify_user_is_human(self):
        pass
    
    def shuffle_user_ids(self, user_ids: list):
        shuffled_ids = random.shuffle(user_ids)
        return shuffled_ids

    def mention_user(self, user_id):
        return "<@" + user_id + ">"
    
    def format_user_ids_into_user_string(self, user_ids):
        member_string = ""

        if len(user_ids) == 0 or not user_ids:
            member_string = "It a-pear-s I'm alone in this channel, maybe remove me?"
        elif len(user_ids) == 1:
            member_string = SINGLE_USER
        elif len(user_ids) % 2 == 0:
            member_string += MESSAGE_HEADER
            for x in range(0, len(user_ids), 2):
                member_string += self.mention_user(user_ids[x]) + " pears with " + self.mention_user(user_ids[x + 1]) + "\n"
        else:
            member_string += MESSAGE_HEADER
            member_string += self.mention_user(user_ids[0]) + " pears with " 
            for x in range(1, len(user_ids), 2):
                member_string += self.mention_user(user_ids[x]) + " pears with " + self.mention_user(user_ids[x + 1]) + "\n"
        print("user list created")
        return member_string

    def post_to_channel(self, user_ids):
        print("post to channel attempted")
        user_string = self.format_user_ids_into_user_string(user_ids=user_ids)
        self.app.client.chat_postMessage(channel=self.CHANNEL_ID, text=user_string)
        print("post to channel active")