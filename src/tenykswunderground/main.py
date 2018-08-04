import asyncio

from tenyksservice import TenyksService, run_service, FilterChain
from tenyksservice.config import settings

from .weather import Weather, NoWeather, UnknownLocation


HELP_TEXT = '''Tenyks Weather:
    All command are direct messages with the bot
    weather <zip or city> - current weather conditions
    weather alerts <zip or city> - current advisories and alerts
    forecast <zip or city> - forecast for the next few days'''


class TenyksWeather(TenyksService):

    irc_message_filters = {
        'weather_alerts': FilterChain([r'^(current\s)?weather alerts (for\s)?(?P<loc>(.*))$', ],
                                      direct_only=True),
        'current_weather': FilterChain([r'^(current\s)?weather (for\s)?(?P<loc>(.*))$', ],
                                       direct_only=True),
        'forecast': FilterChain([r'^forecast (for\s)?(?P<loc>(.*))$', ],
                                      direct_only=True),
        'next': FilterChain([r'^next$', ], direct_only=False),
    }

    help_text = HELP_TEXT
    weather = None
    default_context_timeout = 45

    def __init__(self, *args, **kwargs):
        super(TenyksWeather, self).__init__(*args, **kwargs)
        if not settings.WUNDERGROUND_API_KEY:
            raise Exception("You need to set WUNDERGROUND_API_KEY in settings.py")
        self.weather = Weather(settings.WUNDERGROUND_API_KEY, logger=self.logger)

    def handle_current_weather(self, data, match):
        location = match.groupdict()['loc']

        try:
            current = self.weather.get(self.weather.TYPE_CURRENT, location)
            result = current.string()
        except NoWeather as e:
            self.logger.error(e)
        except UnknownLocation:
            result = 'unknown location'

        self.send(result, data)

    def handle_weather_alerts(self, data, match):
        location = match.groupdict()['loc']
        alerts_to_display = getattr(self.settings, 'DEFAULT_ALERTS', 2)
        results = []

        try:
            alerts = self.weather.get(self.weather.TYPE_ALERTS, location)
            try:
                for i in range(alerts_to_display):
                    results.append(next(alerts).string())

                results.append('find all alerts for this zone here: {}'.format(alerts.zone_alert_page))
                results.append('say "next" for more')

                self.set_expirable_context(
                        data, weather_data=alerts, timeout=self.default_context_timeout)
            except StopIteration:
                pass
        except NoWeather as e:
            self.logger.error(e)
        except UnknownLocation:
            results = ['unknown location']

        for result in results:
            self.send(result, data)

    def handle_forecast(self, data, match):
        location = match.groupdict()['loc']
        days_to_display = getattr(self.settings, 'DEFAULT_FORECAST_DAYS', 2)
        results = []

        try:
            forecast = self.weather.get(self.weather.TYPE_FORECAST, location)

            try:
                for i in range(days_to_display):
                    results.append(next(forecast).string())

                results.append('say "next" for more')

                self.set_expirable_context(
                        data, weather_data=forecast, timeout=self.default_context_timeout)
            except StopIteration:
                pass
        except NoWeather as e:
            self.logger.error(e)
        except UnknownLocation:
            results = ['unknown location']

        
        for result in results:
            self.send(result, data)

    def handle_next(self, data, match):
        ctx = self.get_context(data)
        if ctx:
            try:
                result = next(ctx['weather_data']).string()

                ctx.reset()

                self.send(result, data)
            except StopIteration:
                pass


def main():
    run_service(TenyksWeather)


if __name__ == '__main__':
    main()
