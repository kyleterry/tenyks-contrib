from tenyksservice import TenyksService, run_service

away = {}

class AFK(TenyksService):
    direct_only = False
    irc_message_filters = {
        'depart': [r'^(?i)(xopa|away|afk|brb)'],
        'return': [r'^(?i)(xoka|back)'],
        'query': [r'(?P<nick>(.*))\?$'],
        'list': [r'list']
    }

    def handle_depart(self, data, match):
        self.logger.debug('{nick} went AFK.'.format(nick=data['nick']))
        self.send('{nick} is now AFK.'.format(nick=data['nick']), data)
        away[data['nick']] = True

    def handle_return(self, data, match):
        self.logger.debug('{nick} is no longer AFK.'.format(nick=data['nick']))
        self.send('{nick} is no longer AFK.'.format(nick=data['nick']), data)
        away[data['nick']] = False

    def handle_query(self, data, match):
        nick = match.groupdict()['nick']

        if nick in away:
            status = 'AFK' if away[nick] else 'present'
            self.logger.debug('{nick} is currently {status}'.format(nick=nick, status=status))
            self.send('{nick} is currently {status}.'.format(nick=nick, status=status), data)
        else:
            self.logger.debug('{nick}\' status is unknown.'.format(nick=nick))
            self.send('{nick}\'s status is unknown.'.format(nick=nick), data)

    def handle_list(self, data, match):
        afk_list = {k: v for k, v in away.iteritems() if v}.keys()
        afk_list.sort()
        self.logger.debug('AFKers: {afk}'.format(afk=', '.join(afk_list)))
        self.send('AFKers: {afk}'.format(afk=', '.join(afk_list)), data)


def main():
    run_service(AFK)


if __name__ == '__main__':
    main()
