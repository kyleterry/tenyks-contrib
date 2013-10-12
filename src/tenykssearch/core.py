from tenyks.client import Client, run_client


class TenyksSearch(Client):

    irc_message_filters = {
        'search': r'^search (.*)$',
    }
    direct_only = True

    def handle(self, data, match, filter_name):
        query = match.groups()[0]
        self.send('{nick}: You will be able to search for "{query}" later.'.format(
                    nick=data['nick'], query=query), data=data)


def main():
    search = TenyksSearch()
    run_client(search)


if __name__ == '__main__':
    main()
