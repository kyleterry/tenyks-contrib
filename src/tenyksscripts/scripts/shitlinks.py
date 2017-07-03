import re
from pyxdameraulevenshtein import damerau_levenshtein_distance as edit_distance
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
        num_memes = len(bumps)
        rnd = random.randrange(0, num_memes)
        return get_bump_link(bumps[rnd])
    else:
        return "shit's fucked bro"


def get_stats():
    bumps = get_bumps()
    if bumps:
        return "Total Bumps: {0}".format(len(bumps))
    else:
        return "fuck you there's none"


def get_closest_text_bump(search_text):
    search_text = search_text
    text_bumps = filter(lambda bump: bump['text'], get_bumps())
    if text_bumps:
        min_bump = min(
            text_bumps,
            key=lambda bump: edit_distance(
                bump['text'].lower(),
                search_text
            )
        )
        return get_bump_link(min_bump)
    else:
        return 'no dice m8'


def run(data, settings):
    commands = [
        'dank memes',
        'shithouse stats',
        'dank text'
    ]

    command_regex = re.compile(
        '(?:.*)({0})(?:\s+(.*))?$'.format('|'.join(commands))
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
