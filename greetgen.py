import random


class GreetGenerator:
    def __init__(self):
        self.greets = [
            "Good morning, {}!",
            "Good evening, {}!",
            "Good afternoon, {}!",
            "What's up, {}!",
            "How do you do, {}?",
            "Pleasure to meet you, {}.",
            "Good to see you, {}.",
            "Well, well, well, if it isn't {}.",
            "Whatcha doin', {}?",
            "What are you up to, {}?",
            "Hey {}, how's it going?",
            "{}, what do you think you're doing?"
        ]

    def get_greeting(self):
        return random.choice(self.greets)