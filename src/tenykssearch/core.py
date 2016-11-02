from tenyksservice import TenyksService, run_service, FilterChain


class TenyksSearch(TenyksService):

    irc_message_filters = {
        'search': FilterChain(r'^search (.*)$', direct_only=True),
    }

    def handle(self, data, match, filter_name):
        query = match.groups()[0]
        self.send('{nick}: You will be able to search for "{query}" later.'.format(
                    nick=data['nick'], query=query), data=data)


def main():
    search = TenyksSearch()
    run_service(search)


if __name__ == '__main__':
    main()
