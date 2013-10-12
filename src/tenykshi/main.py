from datetime import date
import random

from tenyks.client import Client, run_client


class TenyksHi(Client):

    direct_only = True

    hellos = ['hi', 'hello', 'hola', 'sup', 'sup?', 'hey', 'heyy', 'heyyy',
              'yo']
    insults = ['shutup', 'stop.', 'you\'re being annoying',
               'I\'m trying to write code']

    def __init__(self, *args, **kwargs):
        self.hello_counts = {}
        super(TenyksHi, self).__init__(*args, **kwargs)

    def handle(self, data, match, filter_name):
        if any([item == data['payload'] for item in self.hellos]):
            if data['nick'] not in self.hello_counts:
                self.hello_counts[data['nick']] = {}
            if date.today() not in self.hello_counts[data['nick']]:
                self.hello_counts[data['nick']][date.today()] = 0

            self.hello_counts[data['nick']][date.today()] += 1

            hello_count = self.hello_counts[data['nick']][date.today()]

            if hello_count < 5:
                self.send('{nick}: {word}'.format(
                    nick=data['nick'], word=random.choice(self.hellos)), data)
            elif hello_count >= 5 and hello_count <= 10:
                self.send('{nick}: {word}'.format(
                    nick=data['nick'], word=random.choice(self.insults)), data)
            elif hello_count == 11:
                self.send('{nick}: I\'m ignoring you.'.format(
                    nick=data['nick']), data)


def main():
    run_client(TenyksHi)


if __name__ == '__main__':
    main()
