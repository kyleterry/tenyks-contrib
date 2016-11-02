import re
import requests
import json
from bs4 import BeautifulSoup
from html.parser import HTMLParser
from tenyksservice import TenyksService, run_service, FilterChain
from tenyksservice.config import settings


class TenyksLinkScraper(TenyksService):

    irc_message_filters = {
        #does not match punctuation at the end of a link. will not match if there is a closing bracket after the link[crude way of ignoring links in parens and a subset of long speils as titles]
        'link_posted': FilterChain([re.compile(r'\b((http|https)://[-A-Za-z0-9+&@#/%?=~_()|!:,.;]*[-A-Za-z0-9+&@#/%=~_()|])[.,]?\s*([^)]*)$').search])
    }

    def handle(*args, **kwargs):
        pass

    def handle_link_posted(self, data, match):
        if settings.POST_URLS.get(data["target"]) is None:
            self.logger.debug(
                'No POST_URLS in the settings for this channel. Cannot post.')
            return None

        if settings.POST_URLS_SALTS.get(data['target']) is None:
            self.logger.debug(
                'No security token for this channel. Cannot post.')
            return None

        url = match.group(1)

        # text after the url is assumed to be a title
        suggested_title = match.group(3)

        submission_salt = settings.POST_URLS_SALTS[data['target']]

        payload = {
            "url": url,
            "person": data['nick'],
            "submission_salt": submission_salt,
        }

        if suggested_title:
            payload["title"] = suggested_title

        post_url = settings.POST_URLS[data["target"]]
        response = requests.post(post_url,
                                 data=json.dumps(payload),
                                 headers={'content-type': 'application/json'})

        if response.status_code != 200:
            self.send('Link Scraper Error: {}'.format(response.text), data)

        self.logger.debug('Posted {url} to {post_url}. Response was {text}. Response code was {code}'.format(
            code=response.status_code,
            url=url,
            text=response.text,
            post_url=post_url))

        if settings.POST_URL_TITLES and \
           settings.POST_URL_TITLES.get(data["target"]):
            head = requests.head(url)
            content_type = head.headers['content-type'].split(' ')[0].strip(';')
            if content_type == 'text/html':
                request = requests.get(url, headers={
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'
                    })
                soup = BeautifulSoup(request.text)
                if soup.title is not None:
                    parser = HTMLParser()
                    title = soup.title.string
                    title = parser.unescape(title)
                    title = title.strip()  # kill newlines and whitespace...
                    self.send('Link title: {}'.format(title), data)


def main():
    run_service(TenyksLinkScraper)

if __name__ == '__main__':
    main()
