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
        self.reset_counters()
        self.lollers = set()

    def reset_counters(self, reset_max=True):
        self.counter = 0
        self.lollers = set()
        if reset_max:
            self.max_chain = random.randint(2,8)
            self.logger.debug("max chain is {}".format(self.max_chain))

    def handle_lol(self, data, match):
        if data["user"] not in self.lollers:
            self.logger.debug("counter at {}".format(self.counter))
            self.counter = self.counter + 1
            self.lollers.add(data["user"])
        
            if self.counter >= self.max_chain:
                self.reset_counters()
                self.logger.debug('spreading the lolbow')
                rainbow = self.create_rainbow()
                self.send(rainbow, data)

    def create_rainbow(self):
        pretty_colors = [4, 5, 7, 9, 10, 11, 12, 13, 14, 15]
        six_rand = (random.choice(pretty_colors) for _ in range(6))
        return "\x03{}L\x03{}O\x03{}L\x03{}B\x03{}O\x03{}W".format(*six_rand)

    def handle_max_chain(self, data, match):
        self.send("{}: max chain is {}, current chain at {}".format(data["nick"], self.max_chain, self.counter), data)


def main():
    run_service(TenyksLol)


if __name__ == '__main__':
    main()
