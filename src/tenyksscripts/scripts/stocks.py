import re
import requests


yql = 'select * from yahoo.finance.quotes where symbol = \'{0}\''
yql_url = 'http://query.yahooapis.com/v1/public/yql'
message = '{name} ({symbol}) {last_price} {change} ({change_percent}) {market_cap}'

def run(data, settings):
    match_re = re.compile(r'^stock (?P<symbol>[\w=]{,10})$').match
    match = match_re(data['payload'])
    if match:
        symbol = match.groupdict()['symbol']
        response = requests.get(yql_url, params={
            'q': yql.format(symbol),
            'env': 'http://datatables.org/alltables.env',
            'format':'json'
        }).json()

        quote = response['query']['results']['quote']
        if quote['ErrorIndicationreturnedforsymbolchangedinvalid']:
            return

        return message.format(**{
            'name': quote['Name'],
            'symbol': quote['symbol'],
            'last_price': quote['LastTradePriceOnly'],
            'change': quote['ChangeRealtime'],
            'change_percent': quote['ChangeinPercent'],
            'market_cap': quote['MarketCapitalization']
        })
