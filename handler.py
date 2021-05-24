import boto3
from slack_bolt import App
from bot import SlackBot

TEST_CHANNEL = "C01U99F6BPW"
LIVE_CHANNEL = "G01PM64DH8C" 

def main(event, context):
    app = get_slackbot_tokens()

    bot = SlackBot(app, TEST_CHANNEL)
    bot.run()

def get_slackbot_tokens():
    client = boto3.client('ssm')

    slack_bot_token = client.get_parameter(
        Name='/mario/pairing-bot/SLACK_BOT_TOKEN',
        WithDecryption=True
    )['Parameter']['Value']

    slack_signing_secret = client.get_parameter(
        Name='/mario/pairing-bot/SLACK_SIGNING_SECRET',
        WithDecryption=True
    )['Parameter']['Value']

    app = App(
        token= slack_bot_token,
        signing_secret= slack_signing_secret
    )

    return app


if __name__ == "__main__":
    main('', '')
