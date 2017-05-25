import re
import random
import requests
import json
try:
    r = requests.get('http://api.shithouse.tv')


    #Solution with json parsing
    parsed_json = json.loads(r.text)
    num_memes = len(parsed_json)
    rnd = random.randrange(0, num_memes)
    if parsed_json[rnd]['nsfw']:
        shit_links = "{nsfw} {bump}.shithouse.tv".format(bump = parsed_json[rnd]['name'], nsfw = "NSFW")
    else:
        shit_links = "{bump}.shithouse.tv".format(bump = parsed_json[rnd]['name'])
except:
    shit_links = "shit's fucked bro"
    num_memes = "fuck you"
def run(data, settings):
    if 'dank memes' in data['payload'].lower():
        return shit_links
#todo add more SICK STATZ
    if 'shithouse stats' in data['payload'].lower():
	return num_memes
