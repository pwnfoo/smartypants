from profane import contains_profanity
import random

class ProfanityFilter:
    def __init__(self):
        self.messages = [
                            'Profanity is bad! Slow down lad.',
                            "Swearing makes up 3 percent of all adult conversation at work and 13 percent of all adult leisure conversation. Don't add up to that :)",
                            "There are empty Petri dishes more cultured than you. Seriously, stop swearing :)",
                            "If you continue using foul words, I'll secretly wish you always have slightly damp socks."
                            ]

    def check_message(self, message):
        if contains_profanity(message):
            return random.choice(self.messages)
        else:
            return False
