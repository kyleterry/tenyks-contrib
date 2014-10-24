from tenyksservice import TenyksService, run_service
from ddate.base import DDate

class DiscordianDate(TenyksService):
    direct_only = True
    irc_message_filters = {
        'today': [r'^(?i)(ddate|discordian)']
    }

    def __init__(self, *args, **kwargs):
        super(DiscordianDate, self).__init__(*args, **kwargs)

    def handle_today(self, data, match):
        self.send(str(DDate()), data)


def main():
    run_service(DiscordianDate)


if __name__ == '__main__':
    main()
