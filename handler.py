from bot import SlackBot

def main(event, context):
    bot = SlackBot()
    bot.run()

if __name__ == "__main__":
    main('', '')
