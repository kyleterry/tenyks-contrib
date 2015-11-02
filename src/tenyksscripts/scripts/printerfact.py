import requests, re

def run(data, settings):
    if data['payload'] == 'printer fact':
        r = requests.get('http://void.vodka/api/')
        fact = r.json()['facts'][0]
        regex = re.compile(re.escape("cat"), re.IGNORECASE)
        return regex.sub("printer", fact)
