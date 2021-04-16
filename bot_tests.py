import unittest
from bot import SlackBot

MESSAGE_HEADER = "You hear a rustling from the fruit bowl nearby. A lone pear within declares: \n\n"

class BotTests(unittest.TestCase):
    def setUp(self):
        self.bot = SlackBot()

    def test_should_mention_user_correctly(self):
        name = "TestBoi"
        result = self.bot.mention_user(name)
        expected_name = "<@TestBoi>"

        self.assertEqual(expected_name, result)

    def test_should_generate_message_for_one_user(self): 
        name = ["TestBoi"]
        result = self.bot.format_user_ids_into_user_string(name)
        expected_output = "You're the only pear on this tree. Best find more fruit friends to pear with!\n" 
        expected_output += "(The pearing bot has only found 1 human user in this channel, feel free to remove it if not in use)."

        self.assertEqual(expected_output, result)

    def test_should_generate_message_for_zero_users(self): 
        name = []
        result = self.bot.format_user_ids_into_user_string(name)
        expected_output = "It a-pear-s I'm alone in this channel, maybe remove me?" 

        self.assertEqual(expected_output, result)

    def test_should_generate_message_for_two_users(self): 
        name = ["David", "Shmavid"]
        result = self.bot.format_user_ids_into_user_string(name)
        expected_output = MESSAGE_HEADER + "<@David> pears with <@Shmavid>\n" 

        self.assertEqual(expected_output, result)

    def test_should_generate_message_for_three_users(self): 
        name = ["David", "Shmavid", "Blavid"]
        result = self.bot.format_user_ids_into_user_string(name)
        expected_output = MESSAGE_HEADER + "<@David> pears with <@Shmavid> pears with <@Blavid>\n" 

        self.assertEqual(expected_output, result)


# for later: "No users have a-pear-ed."


if __name__ == '__main__':
    unittest.main()