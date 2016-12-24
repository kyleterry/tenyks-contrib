from tenyksservice import TenyksService, run_service, FilterChain
import random
from collections import Counter


class TenyksSame(TenyksService):
    irc_message_filters = {
        'same': FilterChain([r"same"],
                           direct_only=False),
        'same_chain':  FilterChain([r"^same chain$"],
                                  direct_only=False),
        'same_leader':  FilterChain([r"^same leader$"],
                                  direct_only=False)
    }

    def __init__(self, name, settings):
        super(TenyksSame, self).__init__(name, settings)
        # store counters, same chains and samers on a per-channel basis
        self.counter = dict()
        self.samers = dict()
        self.last_samer = dict()
        self.same_chain = dict()

    def reset_counters(self, channel, reset_max=True):
        self.counter[channel] = 0
        self.last_samer[channel] = ""
        self.samers[channel] = Counter()
        if reset_max:
            self.same_chain[channel] = random.randint(2, 900)
            self.logger.debug("same chain is {}".format(self.same_chain[channel]))

    def handle_same(self, data, match):
        channel = data["target"]
        # first registered same in this channel (same)
        if channel not in self.samers:
            self.reset_counters(channel)
        if data["user"] not in self.last_samer[channel]:
            self.logger.debug("counter at {}".format(self.counter[channel]))
            self.last_samer[channel] = data["user"]
            self.counter[channel] += 1
            self.samers[channel][data["user"]] += 1

            if self.counter[channel] >= self.same_chain[channel]:
                self.reset_counters(channel)
                self.logger.debug('same')
                samebow = self.create_samebow()
                self.send(samebow, data)

    def create_samebow(self):
        pretty_colors = [4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15]
        random.shuffle(pretty_colors)
        samebow = ["\x03{}same\n".format(pretty_colors.pop()) for _ in range(5)]
        return samebow

    def handle_same_chain(self, data, match):
        channel = data["target"]
        self.send("{}: same chain is {}, current chain at {}".format(
            data["nick"],
            self.same_chain[channel],
            self.counter[channel]), data)

    def handle_same_leader(self, data, match):
        channel = data["target"]

        try:
            leader, second = self.samers[channel].most_common(2)
        except:
            leader, second = [("nobody", "0"), ("void monster", "NULL")]
            leader = self.samers[channel].most_common(1)

        self.send("{}: current same leader is {}, runner up {}".format(
            data["nick"],
            "{}: {}".format(*leader),
            "{}: {}".format(*second)), data)


def main():
    run_service(TenyksSame)


if __name__ == '__main__':
    main()
