import random
import os
import requests
import re

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
PONDERINGS_FILE = SCRIPT_DIR + '/ponderings.txt'


def run(data, settings):
    if hasattr(settings, 'PONDERINGS_FILE') and settings.PONDERINGS_FILE:
        ponderings = settings.PONDERINGS_FILE
    else:
        ponderings = PONDERINGS_FILE

    if data['payload'] == 'give me a creepy url':
        with open(ponderings) as f:
            return random.choice(f.readlines()).strip()
    elif 'add this creepy url' in data['payload']:
        result = add_url_from_payload(data['payload'], ponderings)
        if not result:
            return 'That\'s not a valid url'
        else:
            return 'Aight, I added it.'


def add_url_from_payload(payload, ponderings):
    # get URL out of payload
    re_text = r'^add this creepy url (?P<url>.*)$'
    match = re.compile(re_text).match(payload)
    if match:
        d = match.groupdict()
        url = d['url']
    else:
        return False
    if not is_url(url):
        return False
    with open(ponderings, 'w') as f:
        f.write(url + '\n')
    return True


def is_url(url):
    if not url:
        return False
    url = requests.utils.urlparse(url)
    if not url.scheme and not url.netloc:
        return False
    return True
