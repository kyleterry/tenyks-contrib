import re

import requests

def run(data, settings):
    match_re = re.compile(r'^define (?P<thing>(.*))').match
    match = match_re(data['payload'])
    if match:
        thing = match.groupdict()['thing']
        response = requests.get('https://api.duckduckgo.com/?q=define+{}&format=json'.format(thing))
        response_json = response.json()
        if not response_json:
            return
        if response_json['Definition']:
            definition = []
            if response_json['DefinitionSource']:
                definition.append('[source:{}]'.format(
                    response_json['DefinitionSource']))
            definition.append(response_json['Definition'])
            return ' '.join(definition)
