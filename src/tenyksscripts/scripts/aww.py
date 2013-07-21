import re
import random

import requests

def run(data, settings):
    if re.compile(r'(?i)i( am|\'m) (sad|bummed)').match(
            data['payload']):
        aww_r = requests.get('http://www.reddit.com/r/aww.json')
        aww_json = random.choice(aww_r.json()['data']['children'])
        return 'daaawwwww {url}'.format(url=aww_json['data']['url'])
