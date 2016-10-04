import requests


def run(data, settings):
    if data['payload'] == 'printer fact':
        r = requests.get('https://colbyolson.com/printers')
        if r.status_code == '200':
            return r.text
        else:
            return 'Bad kitty! Endpoint returned HTTP %s' % (r.status_code)
