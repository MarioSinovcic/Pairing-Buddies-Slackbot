import os
import random
import boto3
from slack_bolt import App
from typing import List, Dict

SINGLE_USER_MESSAGE = "You're the only pear on this tree. Best find more fruit friends to pear with!\n(The pearing bot has only found 1 human user in this channel, feel free to remove it if not in use)."
MESSAGE_HEADER = "You hear a rustling from the fruit bowl nearby. A lone pear within declares: \n\n"

TEST_CHANNEL = "C01U99F6BPW"
LIVE_CHANNEL = "G01PM64DH8C" 

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

        self.CHANNEL_ID = TEST_CHANNEL 
        self.app = App(
            token=self.slack_bot_token,
            signing_secret=self.slack_signing_secret
        )

    def run(self) -> None:
        user_ids = self.get_human_user_ids() 
        shuffled_ids = self.shuffle_user_ids(user_ids=user_ids)
        self.post_to_channel(user_ids=user_ids)

    def get_human_user_ids(self) -> List[str]:
        user_ids = self.get_user_ids_from_channel()
        user_ids = self.remove_bots_from_user_ids(user_ids)
        return user_ids

    def get_user_ids_from_channel(self) -> Dict[str, str]:
        response = self.app.client.conversations_members(channel=self.CHANNEL_ID)
        return response['members']

    def remove_bots_from_user_ids(self, user_ids) -> List[str]:
        for user_id in user_ids:
            response = self.app.client.users_info(user=user_id)
            is_bot = response["user"]["is_bot"]
            if is_bot:
                user_ids.remove(user_id)
        return user_ids
    
    def shuffle_user_ids(self, user_ids: list) -> List[str]:
        shuffled_ids = random.shuffle(user_ids)
        return shuffled_ids

    def generate_user_mention_tag(self, user_id) -> str:
        return "<@" + user_id + ">"
    
    def format_user_ids_into_user_string(self, user_ids) -> str:
        member_string = ""

        if len(user_ids) == 0 or not user_ids:
            member_string = "It a-pear-s I'm alone in this channel, maybe remove me?"
        elif len(user_ids) == 1:
            member_string = SINGLE_USER_MESSAGE
        elif len(user_ids) % 2 == 0:
            member_string += MESSAGE_HEADER
            for x in range(0, len(user_ids), 2):
                member_string += self.generate_user_mention_tag(user_ids[x]) + " pears with " + self.generate_user_mention_tag(user_ids[x + 1]) + "\n"
        else:
            member_string += MESSAGE_HEADER
            member_string += self.generate_user_mention_tag(user_ids[0]) + " pears with " 
            for x in range(1, len(user_ids), 2):
                member_string += self.generate_user_mention_tag(user_ids[x]) + " pears with " + self.generate_user_mention_tag(user_ids[x + 1]) + "\n"

        return member_string

    def post_to_channel(self, user_ids) -> None:
        user_string = self.format_user_ids_into_user_string(user_ids=user_ids)
        self.app.client.chat_postMessage(channel=self.CHANNEL_ID, text=user_string)