from os.path import join
import logging
import re
import time
import datetime

from tenyksservice import TenyksService, run_service, FilterChain
from tenyksservice.config import settings

logger = logging.getLogger('tenyks-contrib.gentooservice')


class GentooService(TenyksService):

    irc_message_filters = {
        'get_last_mention': FilterChain([r'^last gentoo mention$']),
        'find_gentoo': FilterChain([re.compile(r'\b(gentoo)\b',
                                               flags=re.IGNORECASE).search]),
        'funroll': FilterChain([re.compile(r'\b(funroll)\b',
                                           flags=re.IGNORECASE).search]),
    }

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

    def handle_funroll(self, data, match):
        self.send('What kinda fun y\'all having?', data)


def main():
    run_service(GentooService)


if __name__ == '__main__':
    main()
