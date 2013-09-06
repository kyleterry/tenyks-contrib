import requests

from tenyksclient.client import Client, run_client
from tenyksclient.config import settings


SEARCH_URL_TEMP = 'http://autocomplete.wunderground.com/aq?query={location}'
CURRENT_COND_TEMP = 'http://api.wunderground.com/api/{api_key}/conditions{query}.json'


class TenyksWeather(Client):

    irc_message_filters = {
        'current_weather': r'current weather (.*)',
    }
    direct_only = True

    def handle_current_weather(self, data, match):
        location = match.groups()[0]
        search = requests.get(SEARCH_URL_TEMP.format(location=location))
        search_json = search.json()
        if search_json['RESULTS']:
            current = requests.get(CURRENT_COND_TEMP.format(
                api_key=settings.WUNDERGROUND_API_KEY,
                query=search_json['RESULTS'][0]['l']))
            current_json = current.json()
            template = '{city} is {temp_f}F ({temp_c}C) and {weather}'
            self.send(template.format(
                city=current_json['current_observation']['display_location']['full'],
                temp_f=current_json['current_observation']['temp_f'],
                temp_c=current_json['current_observation']['temp_c'],
                weather=current_json['current_observation']['weather']), data)
        else:
            self.send('Unknown location', data)


def main():
    run_client(TenyksWeather)


if __name__ == '__main__':
    main()
