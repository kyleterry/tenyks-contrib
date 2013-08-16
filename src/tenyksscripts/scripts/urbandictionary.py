import requests

def run(data, settings):
    if data['payload'] == 'urban dictionary me':
        r = requests.get('http://www.urbandictionary.com/random.php')
        return r.url
