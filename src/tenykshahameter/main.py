# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import time
import re

from tenyksservice import TenyksService, run_service, FilterChain
from tenyksservice.config import settings


class HahaMeter(TenyksService):

    irc_message_filters = {
        'haha': FilterChain(
            [re.compile(r'\b(haha)\b', flags=re.IGNORECASE).search],
            direct_only=False)
    }

    def __init__(self, *args, **kwargs):
        self.HAHAFILE = settings.DATA_WORKING_DIR + '/hahas.db'
        super(HahaMeter, self).__init__(*args, **kwargs)

    def handle_haha(self, data, match):
        self.logger.debug("Haha offender; logging the incident.")
        with open(self.HAHAFILE, 'a+') as f:
            f.write('{} {}\n'.format(int(time.time()), data['nick']))


def main():
    run_service(HahaMeter)


if __name__ == '__main__':
    main()
