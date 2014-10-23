from tenyksservice import TenyksService, run_service

class AFK(TenyksService):
    direct_only = False
    irc_message_filters = {
        'depart': [r'^(?i)(xopa|away|afk|brb)'],
        'return': [r'^(?i)(xoka|back)'],
        'query': [r'(?P<nick>(.*))\?$'],
        'list': [r'list']
    }

    def __init__(self, *args, **kwargs):
        super(AFK, self).__init__(*args, **kwargs)
        self.away = {}

    def handle_depart(self, data, match):
        nick = data['nick']

        if not (nick in self.away and self.away[nick]):
            self.send('{nick} is now AFK.'.format(nick=data['nick']), data)    

        self.away[data['nick']] = True

    def handle_return(self, data, match):
        nick = data['nick']

        if not (nick in self.away and not self.away[nick]):
            self.send('{nick} is no longer AFK.'.format(nick=nick), data)

        self.away[data['nick']] = False

    def handle_query(self, data, match):
        nick = match.groupdict()['nick']

        if nick in self.away:
            status = 'AFK' if self.away[nick] else 'present'
            self.send('{nick} is currently {status}.'.format(nick=nick, status=status), data)
        else:
            self.send('{nick}\'s status is unknown.'.format(nick=nick), data)

    def handle_list(self, data, match):
        afk_list = {k: v for k, v in self.away.iteritems() if v}.keys()

        if len(afk_list) == 0:
            self.send('There are currently no AFKers.', data)
        else:
            afk_list.sort()
            self.send('AFKers: {afk}'.format(afk=', '.join(afk_list)), data)


def main():
    run_service(AFK)


if __name__ == '__main__':
    main()
