from os.path import abspath, join, dirname
import sys
import logging
import re
import time
import datetime

from tenyks.client import Client, run_client
from tenyks.client.config import settings

logger = logging.getLogger('tenyks-contrib.gentooservice')


class GentooService(Client):

    irc_message_filters = {
        'get_last_mention': [r'^last gentoo mention$'],
        'find_gentoo': [re.compile(r'\b(gentoo)\b', flags=re.IGNORECASE).search],
    }

    direct_only = False

    def __init__(self, *args, **kwargs):
        super(GentooService, self).__init__(*args, **kwargs)
        self.filename = 'gentoo_last_mention'

    def handle_find_gentoo(self, data, match):
        last_mention = time.time()
        with open(join(settings.DATA_WORKING_DIR, self.filename), 'w') as f:
            f.write(str(last_mention))

    def handle_get_last_mention(self, data, match):
        try:
            with open(join(settings.DATA_WORKING_DIR, self.filename), 'r') as f:
                self.send(str(datetime.datetime.fromtimestamp(float(f.read()))), data)
        except IOError:
            self.send('Wow... Never.', data)

def main():
    run_client(GentooService)


if __name__ == '__main__':
    main()
