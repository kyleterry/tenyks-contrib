import requests, re

def run(data, settings):
    if data['payload'] == 'printer fact':
        r = requests.get('https://colbyolson.com/printers')
        return r.text
