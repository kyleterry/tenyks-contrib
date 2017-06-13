import random
import requests
import json


def gimme():
    try:
        r = requests.get('http://api.shithouse.tv')

        # Solution with json parsing
        parsed_json = json.loads(r.text)
        num_memes = len(parsed_json)
        rnd = random.randrange(0, num_memes)
        shit_link = []

        if parsed_json[rnd]['nsfw']:
            shit_link.append('\x0304[NSFW]\x0F')

        shit_link.append('\x0310http://{0}.shithouse.tv'.format(parsed_json[rnd]['name']))
    except:
        shit_link = "shit's fucked bro"
        num_memes = "fuck you there's none"

    return (' '.join(shit_link), num_memes)


def run(data, settings):
    answer = gimme()

    if 'dank memes' in data['payload'].lower():
        return answer[0]

    # todo add more SICK STATZ
    if 'shithouse stats' in data['payload'].lower():
        return "Total Bumps: {0}".format(answer[1])
