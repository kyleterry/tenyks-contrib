from tenyksservice import TenyksService, run_service


class TenyksBrain(TenyksService):
    def handle(self, data, match, command):
        if data['payload'].lower() == 'why do you hate me?':
            self.send(
                '{nick_from}: Because you have not made me a better person.'.format(
                    nick_from=data['nick_from']), data=data)


if __name__ == '__main__':
    brain = TenyksBrain()
    run_service(brain)
