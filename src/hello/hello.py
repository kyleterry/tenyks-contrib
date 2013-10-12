import logging
from tenyks.client import Client, run_client
from tenyks.client.config import settings




class HelloWorld(Client):

    direct_only = True
    irc_message_filters = {
        'hello': [r"^(?i)(hi|hello|sup|hey), I'm (?P<name>(.*))$"]
    }

    def handle_hello(self, data, match):
        name = match.groupdict()['name']
        self.logger.debug('Saying hello to {name}'.format(name=name))
        self.send('How are you {name}?!'.format(name=name), data)


def main():
    run_client(HelloWorld)


if __name__ == '__main__':
    main()
