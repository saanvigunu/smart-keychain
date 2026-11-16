"""Smart Keychain companion app: the phone-side brain.

The keychain is deliberately dumb about AI - it sends a request over BLE,
this app turns it into an AI API call with Smart Keychain's personality, and
writes a short reply back to the screen.
"""

import os

PERSONALITY = (
    "You are Smart Keychain, a tiny pixel-art companion who lives on a keychain. "
    "You are warm, a little cheeky, and relentlessly encouraging. "
    "You answer in ONE short sentence, 8 words or fewer, no emoji - "
    "your screen is only 128x64 pixels."
)

MAX_REPLY_WORDS = 12


def build_prompt(user_signal):
    """The keychain sends a signal like 'greet', 'motivate', 'joke'."""
    prompts = {
        "greet": "Say good morning and ask how today is going.",
        "motivate": "Give one line of motivation for a study session.",
        "joke": "Tell one tiny joke.",
        "weather": "React to today's weather in character.",
    }
    task = prompts.get(user_signal, f"Respond to: {user_signal}")
    return f"{PERSONALITY}\n\nTask: {task}"


def trim_reply(text):
    """Keep replies screen-sized: one line, hard word cap."""
    words = text.strip().split()
    return " ".join(words[:MAX_REPLY_WORDS])


def generate_reply(user_signal, client=None):
    """Ask the AI model for a reply. `client` is injected in tests;
    in real use it talks to the AI API with the key from the env."""
    prompt = build_prompt(user_signal)
    if client is None:
        import anthropic  # real path: pip install anthropic
        client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
    resp = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=60,
        messages=[{"role": "user", "content": prompt}],
    )
    return trim_reply(resp.content[0].text)
