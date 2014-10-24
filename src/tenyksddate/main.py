import datetime
from tenyksservice import TenyksService, run_service
from ddate.base import DDate

class DiscordianDate(TenyksService):
    direct_only = True
    irc_message_filters = {
        'date': [
            r'^(?i)(ddate|discordian) (?P<month>(.*)) (?P<day>(.*)) (?P<year>(.*))',
            r'^(?i)(ddate|discordian) (?P<month>(.*))-(?P<day>(.*))-(?P<year>(.*))',
            r'^(?i)(ddate|discordian) (?P<month>(.*))/(?P<day>(.*))/(?P<year>(.*))'
        ],
        'today': [r'^(?i)(ddate|discordian)']
    }

    def __init__(self, *args, **kwargs):
        super(DiscordianDate, self).__init__(*args, **kwargs)

    def handle_date(self, data, match):
        year = int(match.groupdict()['year'])
        month = int(match.groupdict()['month'])
        day = int(match.groupdict()['day'])

        self.send(str(DDate(datetime.date(year=year, month=month, day=day))), data)

    def handle_today(self, data, match):
        self.send(str(DDate()), data)


def main():
    run_service(DiscordianDate)


if __name__ == '__main__':
    main()
