import random

smiles = [':^)', ':-D', ':D', ':)', ':P', '(^:', 'B-)', ';)', '(;']
frowns = [':^(', 'D-:', 'D:', ':(', ':-/', ')^:', 'B-(', ':\'(']


def run(data, settings):
    if data['payload'] in smiles:
        return random.choice(smiles)
    if data['payload'] in frowns:
        return random.choice(frowns)
