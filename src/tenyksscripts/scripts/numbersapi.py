import re

import requests

def run(data, settings):
    match_re = re.compile(r'^random (?P<fact_type>(.*)) fact').match
    match = match_re(data['payload'])
    if match:
        fact_type = match.groupdict()['fact_type']
        r = requests.get('http://numbersapi.com/random/{}'.format(fact_type))
        return r.text
