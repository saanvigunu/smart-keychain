import unittest
from unittest.mock import MagicMock

from companion.personality import (MAX_REPLY_WORDS, PERSONALITY,
                                   build_prompt, generate_reply, trim_reply)


class PromptTests(unittest.TestCase):
    def test_known_signals_have_canned_tasks(self):
        self.assertIn("motivation", build_prompt("motivate"))
        self.assertIn("joke", build_prompt("joke"))

    def test_unknown_signal_passes_through(self):
        self.assertIn("homework", build_prompt("homework"))

    def test_personality_caps_length(self):
        self.assertIn("8 words or fewer", PERSONALITY)


class TrimTests(unittest.TestCase):
    def test_short_reply_untouched(self):
        self.assertEqual(trim_reply("you got this"), "you got this")

    def test_long_reply_capped(self):
        long = "word " * 40
        self.assertEqual(len(trim_reply(long).split()), MAX_REPLY_WORDS)

    def test_whitespace_normalized(self):
        self.assertEqual(trim_reply("  hi   there  "), "hi there")


class GenerateTests(unittest.TestCase):
    def test_generate_with_mock_client(self):
        client = MagicMock()
        block = MagicMock()
        block.text = "small steps still move mountains friend"
        client.messages.create.return_value.content = [block]
        reply = generate_reply("motivate", client=client)
        self.assertEqual(reply, "small steps still move mountains friend")
        prompt = client.messages.create.call_args.kwargs["messages"][0]["content"]
        self.assertIn("Smart Keychain", prompt)

    def test_generate_trims_overflow(self):
        client = MagicMock()
        block = MagicMock()
        block.text = " ".join(f"w{i}" for i in range(50))
        client.messages.create.return_value.content = [block]
        self.assertEqual(len(generate_reply("greet", client=client).split()),
                         MAX_REPLY_WORDS)


if __name__ == "__main__":
    unittest.main()
