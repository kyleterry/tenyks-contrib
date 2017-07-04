import re
from fuzzywuzzy import process, fuzz
import random
import requests
import json


def get_bump_link(bump):
    shit_link = []
    if bump['nsfw']:
        shit_link.append('\x0304[NSFW]\x0F')

    shit_link.append('\x0310http://{0}.shithouse.tv'.format(bump['name']))
    return ' '.join(shit_link)


def get_bumps():
    try:
        return json.loads(requests.get('http://api.shithouse.tv').text)
    except:
        return []


def get_random_bump():
    bumps = get_bumps()
    if bumps:
        return get_bump_link(random.choice(bumps))
    else:
        return "shit's fucked bro"


def get_stats():
    bumps = get_bumps()
    if bumps:
        return "Total Bumps: {0}".format(len(bumps))
    else:
        return "fuck you there's none"


def get_closest_text_bump(search_text):
    search_text = {'text': search_text}
    text_bumps = filter(lambda bump: bump['text'], get_bumps())
    if text_bumps:
        best_bumps = process.extractBests(
            search_text,
            text_bumps,
            scorer=fuzz.token_set_ratio,
            processor=lambda bump: bump['text'].lower()
        )
        best_bumps = [
            bump[0]
            for bump in best_bumps
            if bump[1] == best_bumps[0][1]
        ]
        return get_bump_link(random.choice(best_bumps))
    else:
        return 'no dice m8'


def run(data, settings):
    commands = [
        'dank memes',
        'shithouse stats',
        'dank text'
    ]

    command_regex = re.compile(
        '(?:.*?)({0})(?:\s+(.*))?$'.format('|'.join(commands))
    )

    match = command_regex.match(data['payload'].lower())

    if match:
        groups = match.groups()
        command = groups[0]

        if command == 'dank memes':
            return get_random_bump()

        # todo add more SICK STATZ
        elif command == 'shithouse stats':
            return get_stats()

        elif command == 'dank text':
            if groups[1]:
                return "Closest result for '{0}': {1}".format(
                    groups[1],
                    get_closest_text_bump(groups[1])
                )
            else:
                return 'gimme a string to search'
