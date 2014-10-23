from tenyksservice import TenyksService, run_service


class AFK(TenyksService):
    direct_only = True
    irc_message_filters = {
        'away': [r'^(?i)(away|afk) (?P<name>(.*))$']
    }

    def handle_away(self, data, match):
        name = match.groupdict()['name']
        self.logger.debug('Checking if {name} is away.'.format(name=name))
        self.send('{name} is currently AFK.'.format(name=name), data)


def main():
    run_service(AFK)


if __name__ == '__main__':
    main()
