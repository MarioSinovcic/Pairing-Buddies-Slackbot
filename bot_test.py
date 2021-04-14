import unittest
from bot import SlackBot

class BotTests(unittest.TestCase):
    def setUp(self):
        self.bot = SlackBot()

    def test_if_users_in_channel_exist(self):
        self.assertTrue(len(self.bot.users) > 0)