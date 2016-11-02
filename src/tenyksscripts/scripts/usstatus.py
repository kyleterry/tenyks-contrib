from datetime import datetime
import re
import requests
from bs4 import BeautifulSoup


def run(data, settings):
    if data['payload'] == 'US status':
        req = requests.get('http://govuptime.com')

        soup = BeautifulSoup(req.text)
        yesno = soup.select('h2 + p')[0].text
        if re.search('no', yesno, re.IGNORECASE):
            return 'The federal government is having problems as of {}'.format(
                str(datetime.now()))
        else:
            return 'The federal government is up as of {}'.format(
                str(datetime.now()))

if __name__ == '__main__':
    print(run({'payload': 'US status'}, []))
