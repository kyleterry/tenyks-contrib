import random

portland_facts = [
        "You didn't know?",
]

def run(data, settings):
    if (data['payload'] == 'portland fact') or (data['payload'] == 'Portland fact'):
        return random.choice(portland_facts)
