import requests, re

def run(data, settings):
    if data['payload'] == 'printer fact':
        r = requests.get('https://catfacts-api.appspot.com/api/facts?number=1')
        fact = r.json()['facts'][0]
        regex = re.compile(re.escape("cat"), re.IGNORECASE)
        return regex.sub("printer", fact)
