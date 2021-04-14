import unittest
from bot import SlackBot

class BotTests(unittest.TestCase):
    def setUp(self):
        self.bot = SlackBot()

    def test_bot_returns_correct_user_list(self):
        self.assertTrue(len(self.bot.users) > 0)

if __name__ == '__main__':
    unittest.main()