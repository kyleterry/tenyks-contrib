import requests

def run(data, settings):
    if data['payload'] == 'cat fact':
        r = requests.get('https://catfacts-api.appspot.com/api/facts?number=1')
        return r.json()['facts'][0]
