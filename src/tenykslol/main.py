from tenyksservice import TenyksService, run_service, FilterChain
import random

class TenyksLol(TenyksService):
    irc_message_filters = {
        'lol': FilterChain([r"lol"],
                             direct_only=False),
        'max_chain':  FilterChain([r"^max chain$"],
                                 direct_only=False)
    }
    
    def __init__(self, name, settings):
        super(TenyksLol, self).__init__(name, settings)
        # store counters, max chains and lollers on a per-channel basis
        self.lollers = dict()
        self.counter = dict()
        self.max_chain = dict()

    def reset_counters(self, channel, reset_max=True):
        self.counter[channel] = 0
        self.lollers[channel] = set()
        if reset_max:
            self.max_chain[channel] = random.randint(2,9)
            self.logger.debug("max chain is {}".format(self.max_chain[channel]))

    def handle_lol(self, data, match):
        channel = data["target"]
        # first registered laugh in this channel (wow sad)
        if channel not in self.lollers:
            self.reset_counters(channel)
        if data["user"] not in self.lollers[channel]:
            self.logger.debug("counter at {}".format(self.counter[channel]))
            self.counter[channel] = self.counter[channel] + 1
            self.lollers[channel].add(data["user"])
        
            if self.counter[channel] >= self.max_chain[channel]:
                self.reset_counters(channel)
                self.logger.debug('spreading the lolbow')
                rainbow = self.create_rainbow()
                self.send(rainbow, data)

    def create_rainbow(self):
        pretty_colors = [4, 5, 7, 9, 10, 11, 12, 13, 14, 15]
        six_rand = (random.choice(pretty_colors) for _ in range(6))
        return "\x03{}L\x03{}O\x03{}L\x03{}B\x03{}O\x03{}W".format(*six_rand)

    def handle_max_chain(self, data, match):
        channel = data["target"]
        self.send("{}: max chain is {}, current chain at {}".format(data["nick"], self.max_chain[channel],
            self.counter[channel]), data)


def main():
    run_service(TenyksLol)


if __name__ == '__main__':
    main()
