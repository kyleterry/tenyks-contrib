import random

dark_things = [
    'Everyone you know will eventually be dead.',
    'One day your name will be said for the last time.',
    'People die over money. It\'s such a useless things, but people are still dying',
    'Chuck Noris isn\'t special. His round-house can\'t destroy the moon and his sexual penetration didn\'t birth the 1972 Miami Dolphins.',
]


def run(data, settings):
    if data['payload'] == 'tell me something dark':
        return random.choice(dark_things)
