import requests

'''
{ 
    "message":"Download the latest version at noctuelles.net!",
    "connections":1,
    "activegames":1,
    "servers":[
        {
            "id":"91",
            "players":"1",
            "ip":"94575592176649461",
            "map":"pi_set",
            "version":"5"
        }
    ]
}
'''
def run(data, settings):
    message = data['payload']
    key = None

    if message.startswith('wfh'):
        key = 'wfh'
    elif message.startswith('anubis'):
        key = 'anu'
    else:
        return None

    url = "http://api.xxiivv.com/?key={0}&cmd=read".format(key)
    r = requests.get(url)
    data = r.json()

    if 'server' in message:
        return "There are {} active servers.".format(len(data['servers']))
    elif 'player count' in message:
        return "There are {} players.".format(
            reduce(
                lambda acc, val: acc + int(val['players']),
                data['servers'],
                0
            ))
    elif 'games' in message:
        return "There are {} games.".format(data['activegames'])

