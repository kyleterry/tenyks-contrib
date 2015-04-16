import random

smiles = [':^)', ':-D', ':)', ':P', '(^:', 'B-)']


def run(data, settings):
    if ':^)' == data['payload']:
        return random.choice(smiles)
