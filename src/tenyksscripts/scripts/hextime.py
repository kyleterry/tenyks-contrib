from datetime import datetime


def run(data, settings):
    if data['payload'] == 'current time in hex':
        now = datetime.now()
        return '{hour}:{minute}:{second}'.format(
            hour=hex(now.hour), minute=hex(now.minute), second=hex(now.second))
