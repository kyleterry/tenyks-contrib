from os.path import abspath, join, dirname
import sys
import logging

from tenyksservice import TenyksService, run_service, FilterChain
from tenyksservice.config import settings

logger = logging.getLogger('tenyks-contrib.tenyksscripts')


class TenyksScripts(TenyksService):

    irc_message_filters = {
        'list_scripts': FilterChain([r'list scripts'], direct_only=True)
    }

    pass_on_non_match = True


    def __init__(self, *args, **kwargs):
        super(TenyksScripts, self).__init__(*args, **kwargs)

        self.running_scripts = list()

        sys.path.append(abspath(dirname(__file__)))

        for script in settings.SCRIPTS:
            callback = self._fetch_script_callback(script)
            if callback:
                logger.info('{script} is now live'.format(script=script))
                self.running_scripts.append(callback)

    def _fetch_script_callback(self, script_name):
        callback_module = __import__(script_name, fromlist=['handler'])
        return callback_module.run

    def handle_list_scripts(self, data, match):
        pass

    def handle(self, data, match, filter_name):
        for callback in self.running_scripts:
            message = callback(data, settings)
            if message:
                self.send(message, data)


def main():
    run_service(TenyksScripts)


if __name__ == '__main__':
    main()
