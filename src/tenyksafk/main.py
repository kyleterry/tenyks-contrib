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
        away[data['nick']] = True
        self.send('{nick} is now AFK.'.format(nick=data['nick']), data)

    def handle_return(self, data, match):
        away[data['nick']] = False
        self.send('{nick} is no longer AFK.'.format(nick=data['nick']), data)

    def handle_query(self, data, match):
        nick = match.groupdict()['nick']

        if nick in away:
            status = 'AFK' if away[nick] else 'present'
            self.send('{nick} is currently {status}.'.format(nick=nick, status=status), data)
        else:
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
