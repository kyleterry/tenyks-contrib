import random

def run(data, settings):
    if data['payload'] == 'roll':
        roll = random.randint(1, 6)
        return roll
