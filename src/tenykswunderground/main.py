import requests

from tenyksservice import TenyksService, run_service, FilterChain
from tenyksservice.config import settings


SEARCH_URL_TEMPLATE = 'http://autocomplete.wunderground.com/aq?query={location}'
CURRENT_COND_TEMPLATE = 'http://api.wunderground.com/api/{api_key}/conditions{query}.json'
# Example: Portland, OR is 56.1 F (13.4 C) and Overcast; windchill is NA; winds are Calm
ALERTS_TEMPLATE = 'http://api.wunderground.com/api/{api_key}/alerts{query}.json'
FORECAST_TEMPLATE = 'http://api.wunderground.com/api/{api_key}/forecast{query}.json'

TYPE_CURRENT = 'current'
TYPE_ALERTS = 'alerts'
TYPE_FORECAST = 'forecast'


class TenyksWeather(TenyksService):

    irc_message_filters = {
        'current_weather': FilterChain([r'^(current\s)?weather (for\s)?(?P<loc>(.*))$', ],
                                       direct_only=True),
        'weather_alerts': FilterChain([r'^(current\s)?weather alerts (for\s)?(?P<loc>(.*))$', ],
                                      direct_only=True),
        'forecast': FilterChain([r'^forecast (for\s)?(?P<loc>(.*))$', ],
                                      direct_only=True),
    }

    def __init__(self, *args, **kwargs):
        super(TenyksWeather, self).__init__(*args, **kwargs)
        if not settings.WUNDERGROUND_API_KEY:
            raise Exception("You need to set WUNDERGROUND_API_KEY in settings.py")

    def fetch_location(self, location_query):
        search = requests.get(SEARCH_URL_TEMPLATE.format(location=location_query))
        search_json = search.json()
        if search_json['RESULTS']:
            return search_json['RESULTS'][0]['l']
        return None

    def fetch_weather_data(self, data_type, location_string):
        if data_type == TYPE_CURRENT:
            data = requests.get(CURRENT_COND_TEMPLATE.format(
                api_key=settings.WUNDERGROUND_API_KEY,
                query=location_string))
        elif data_type == TYPE_ALERTS:
            data = requests.get(ALERTS_TEMPLATE.format(
                api_key=settings.WUNDERGROUND_API_KEY,
                query=location_string))
        elif data_type == TYPE_FORECAST:
            data = requests.get(FORECAST_TEMPLATE.format(
                api_key=settings.WUNDERGROUND_API_KEY,
                query=location_string))
        if data.status_code == 200:
            return data.json()

    def handle_current_weather(self, data, match):
        location = match.groupdict()['loc']
        location_string = self.fetch_location(location)
        if location_string:
            current_json = self.fetch_weather_data(TYPE_CURRENT, location_string)
            if current_json:
                template = '{city} is {temp} and {weather}; windchill is {chill}; winds are {wind}'
                self.send(template.format(
                    city=current_json['current_observation']['display_location']['full'],
                    temp=current_json['current_observation']['temperature_string'],
                    weather=current_json['current_observation']['weather'],
                    chill=current_json['current_observation']['windchill_string'],
                    wind=current_json['current_observation']['wind_string']), data)
        else:
            self.send('Unknown location', data)

    def handle_weather_alerts(self, data, match):
        location = match.groupdict()['loc']
        location_string = self.fetch_location(location)
        if location_string:
            alerts_json = self.fetch_weather_data(TYPE_ALERTS, location_string)
            if alerts_json and alerts_json['alerts']:
                top_alert = alerts_json['alerts'][0]
                print top_alert
                template = '{advisory} - {message}'
                self.send(template.format(
                    advisory=top_alert['description'],
                    message=top_alert['message'][0:600].replace('\n', '')), data)
            else:
                self.send('No alerts.', data)
        else:
            self.send('Unknown location', data)

    def handle_forecast(self, data, match):
        location = match.groupdict()['loc']
        location_string = self.fetch_location(location)
        if location_string:
            forecast_json = self.fetch_weather_data(
                TYPE_FORECAST, location_string)
            if forecast_json:
                template = '{day} - {message}'
                i = 0
                for day in forecast_json['forecast']['txt_forecast']['forecastday']:
                    if i < 5:
                        self.send(template.format(
                            day=day['title'], message=day['fcttext']), data)
                    else:
                        break
                    i = i + 1
        else:
            self.send('Unknown location', data)


def main():
    run_service(TenyksWeather)


if __name__ == '__main__':
    main()
