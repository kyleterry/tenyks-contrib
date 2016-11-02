import random

from tenyksservice import TenyksService, run_service


class TenyksOutOfContext(TenyksService):

    def __init__(self):
        super(TenyksOutOfContext, self).__init__()
        self.messages = {}
        self.choices = [
            'I burnt my tongue.',
            'So that\'s where babies come from...',
            'I\'m sleepy',
            'If a farting wiener dog ever falls into a deep puddle we are all fucked.',
        ]

    def handle(self, data, match, filter_name):
        if data['irc_channel'].startswith('#'):
            try:
                count = self.messages[data['connection_name']][data['irc_channel']]
                self.messages[data['connection_name']][data['irc_channel']] = count + 1
            except:
                count = 0
                self.messages[data['connection_name']] = {
                    data['irc_channel']: count}
            self.logger.debug('{conn}:{channel} message count: {count}'.format(
                conn=data['connection_name'], channel=data['irc_channel'],
                count=self.messages[data['connection_name']][data['irc_channel']]))
            self.last_nick = data['nick_from']
            if count + 1 >= 10:
                self.send(random.choice(self.choices), data)
                self.messages[data['connection_name']][data['irc_channel']] = 0


def main():
    out_of_context = TenyksOutOfContext()
    run_service(out_of_context)


if __name__ == '__main__':
    main()
