## WARNING: If the title of a page has a URL, this may cause a feedback loop

# In [3]: urltitle.run({'payload': 'http://google.com'}, [])
# Out[3]: u'Google'
# 
# In [4]: urltitle.run({'payload': 'hur hur, check this out: http://4chan.org'}, [])
# Out[4]: u'4chan'

import re
import requests
from BeautifulSoup import BeautifulSoup

url_regex = "(?P<url>https?://[^\s]+)"

def run(data, settings):

    # Get the URL
    match = re.search(url_regex, data['payload'])
    if not match:
        return
    url = match.group('url')

    # Load URL, and parse HTML
    request = requests.get(url)
    soup = BeautifulSoup(request.text)

    # Return title
    return soup.title.string
