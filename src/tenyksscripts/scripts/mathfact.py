import requests

def run(data, settings):
    if data['payload'] == 'math fact':
        r = requests.get('http://numbersapi.com/random/math')
        return r.text
