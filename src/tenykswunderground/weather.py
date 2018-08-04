from collections import defaultdict
import textwrap
import dateutil.parser

import requests


class NoWeather(Exception):
    pass


class UnknownLocation(Exception):
    pass


class Weather:
    TYPE_CURRENT = 'current'
    TYPE_ALERTS = 'alerts'
    TYPE_FORECAST = 'forecast'

    api_key = None

    def __init__(self, api_key, logger=None):
        self.api_key = api_key

        self._logger = logger

    def get(self, data_type, location):
        if data_type == self.TYPE_CURRENT:
            return CurrentWeather(self.api_key, location, logger=self._logger)
        elif data_type == self.TYPE_ALERTS:
            return CurrentAlerts(self.api_key, location, logger=self._logger)
        elif data_type == self.TYPE_FORECAST:
            return CurrentForecast(self.api_key, location, logger=self._logger)

        return None


class APIFetcher:
    def __init__(self, url, logger=None):
        self._logger = logger
        self._url = url

    def fetch(self):
        if self._logger:
            self._logger.debug('fetching weather data from: {}'.format(self._url))
        data = requests.get(self._url)
        if data.status_code == 200:
            return data.json()
        raise NoWeather('request to weather api failed with status code: {}'.format(data.status_code))


class LocationSearch:

    wu_query_endpoint = 'https://autocomplete.wunderground.com/aq?query={location}'

    def __init__(self, api_key, location_string, logger=None):
        url = self.wu_query_endpoint.format(location=location_string)
        self.fetcher = APIFetcher(url, logger=logger)

    def search(self):
        search_json = self.fetcher.fetch()
        if search_json['RESULTS']:
            return Bunch(search_json['RESULTS'][0])
        raise UnknownLocation


class CurrentWeather:

    wu_conditions_endpoint = 'https://api.wunderground.com/api/{api_key}/conditions{query}.json'

    def __init__(self, api_key, location_string, logger=None):
        location = LocationSearch(api_key, location_string, logger=logger).search()

        format_dict = {'api_key': api_key, 'query': location.l}
        url = self.wu_conditions_endpoint.format(**format_dict)
        fetcher = APIFetcher(url, logger=logger)
        data = fetcher.fetch()
        
        co = data['current_observation']

        self.location = Bunch(co['display_location'])
        self.temperature = co['temperature_string']
        self.weather = co['weather']
        self.wind = 'no wind :^)' if co['wind_string'] is 'NA' else co['wind_string']
        self.windchill = None if co['windchill_string'] is 'NA' else co['windchill_string']

    def string(self):
        return '{} [ {} {}; winds: {} ]'.format(self.location.full, self.temperature, self.weather, self.wind)


class CurrentAlerts:

    nws_points_endpoint = 'https://api.weather.gov/points/{lat},{long}'
    nws_alerts_endpoint = 'https://api.weather.gov/alerts/?active=1&zone={zone}'
    nws_zone_alert_page = 'https://alerts.weather.gov/cap/wwaatmget.php?x={zone}&y=1'

    def __init__(self, api_key, location_string, logger=None):
        self.location = LocationSearch(api_key, location_string, logger=logger).search()

        url = self.nws_points_endpoint.format(lat=self.location.lat, long=self.location.lon)
        point = APIFetcher(url, logger=logger).fetch()

        forecast_zone = APIFetcher(point['properties']['forecastZone']).fetch()
        self.zone = forecast_zone['properties']['id']

        alerts_url = self.nws_alerts_endpoint.format(zone=forecast_zone['properties']['id'])
        data = APIFetcher(alerts_url, logger=logger).fetch()

        self._alerts = iter(data['features'])
        self._current = None

    def __iter__(self):
        return self

    def __next__(self):
        self._current = next(self._alerts)
        return self

    @property
    def zone_alert_page(self):
        return self.nws_zone_alert_page.format(zone=self.zone)

    def string(self):
        properties = self._current['properties']

        headline = ' '.join(properties['parameters']['NWSheadline'])
        start = dateutil.parser.parse(properties['effective'])
        end = dateutil.parser.parse(properties['expires'])
        return '{} [ {}({}): FROM {} TO {} -- {} ]'.format(
                self.location.name,
                properties['event'],
                properties['severity'],
                start.strftime('%b %d %X'),
                end.strftime('%b %d %X'),
                textwrap.shorten(headline, width=200))


class CurrentForecast:

    wu_forecast_endpoint = 'http://api.wunderground.com/api/{api_key}/forecast{query}.json'

    def __init__(self, api_key, location_string, logger=None):
        self.location = LocationSearch(api_key, location_string, logger=logger).search()

        format_dict = {'api_key': api_key, 'query': self.location.l}
        url = self.wu_forecast_endpoint.format(**format_dict)
        fetcher = APIFetcher(url, logger=logger)
        data = fetcher.fetch()

        fd = data['forecast']['txt_forecast']['forecastday']

        self._forecast_lines = iter(self.make_lines(fd))
        self._current = None

    def __iter__(self):
        return self

    def __next__(self):
        self._current = next(self._forecast_lines)
        return self

    def make_lines(self, data):
        d = defaultdict(list)

        for day, data in [(day['title'].split().pop(0), day) for day in data]:
            d[day].append(data)

        return list(d.items())

    def string(self):
        day, forecasts = self._current
        descriptions = [fc['fcttext'] for fc in forecasts]

        return '{} [ {}: {} ]'.format(
            self.location.name,
            day,
            ' -- '.join(descriptions))


class Bunch(object):
  def __init__(self, adict):
    self.__dict__.update(adict)
