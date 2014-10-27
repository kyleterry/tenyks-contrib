import datetime
from tenyksservice import TenyksService, FilterChain, run_service
from ddate.base import DDate

class DiscordianDate(TenyksService):
    irc_message_filters = {
        'usage': FilterChain([r'^(?i)(ddate|discordian) (?i)(usage|help)'], direct_only=True),
        'date': FilterChain([
            r'^(?i)(ddate|discordian) (?P<month>(.*)) (?P<day>(.*)) (?P<year>(.*))',
            r'^(?i)(ddate|discordian) (?P<month>(.*))-(?P<day>(.*))-(?P<year>(.*))',
            r'^(?i)(ddate|discordian) (?P<month>(.*))/(?P<day>(.*))/(?P<year>(.*))'
        ], direct_only=True),
        'today': FilterChain([r'^(?i)(ddate|discordian)'], direct_only=True)
    }

    def __init__(self, *args, **kwargs):
        super(DiscordianDate, self).__init__(*args, **kwargs)

    def handle_usage(self, data, match):
        self.send('Accepted formats: mm dd yyyy, mm-dd-yyyy, mm/dd/yyyy', data)

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
