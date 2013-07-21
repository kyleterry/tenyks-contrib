def run(data, settings):
    if 'ping' == data['payload']:
        return 'pong'
