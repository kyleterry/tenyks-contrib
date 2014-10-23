from tenyksservice import TenyksService, run_service


class AFK(TenyksService):
    direct_only = False
    irc_message_filters = {
        'depart': [r'^(?i)(xopa|away|afk|brb)'],
        'return': [r'^(?i)(xoka|back)']
    }

    def handle_depart(self, data, match):
        self.logger.debug('{nick} went AFK.'.format(nick=data['nick']))
        self.send('{nick} is now AFK.'.format(nick=data['nick']), data)

    def handle_return(self, data, match):
        self.logger.debug('{nick} is no longer AFK.'.format(nick=data['nick']))
        self.send('{nick} is no longer AFK.'.format(nick=data['nick']), data)


def main():
    run_service(AFK)


if __name__ == '__main__':
    main()
