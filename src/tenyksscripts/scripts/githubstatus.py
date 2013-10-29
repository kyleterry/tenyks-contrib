import requests


def run(data, settings):
    if data['payload'] == 'github status':
        status_url = 'https://status.github.com/api/status.json'
        last_message_url = 'https://status.github.com/api/last-message.json'
        status = requests.get('https://status.github.com/api/status.json').json()
        if status['status'] in ('minor', 'major'):
            last_message = requests.get(last_message_url)
            return 'Github is having problems as of {timestamp}: {message}'.format(
                    timestamp=last_message['created_on'], message=last_message['body'])
        else:
            return 'Github.com is up as of {timestamp}'.format(
                    timestamp=status['last_updated'])

