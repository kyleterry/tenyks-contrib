import requests
from tenyksclient.client import Client, run_client, settings


class TenyksLinkScraper(Client):

    direct_only = False
    irc_message_filters = {
        'link_posted': [r'\(?\b(http|https)://[-A-Za-z0-9+&@#/%?=~_()|!:,.;]*[-A-Za-z0-9+&@#/%=~_()|]'],
    }

    def handle_link_posted(self, data, match):
        if settings.POST_URL is None:
            self.logger.debug('No POST_URL in the settings for this service. Cannot post.')
            return None

        url = match.groups(0)[0]
        payload = '{"url": "%s", "person": "%s"}' % (match.groups(0)[0], data['nick'])

        req = requests.post(settings.POST_URL,
            data=payload,
            headers={'content-type': 'application/json'})

        self.logger.debug('Posted {url} to {post_url}. Response code was {code}'.format(
            code=unicode(req.status_code),
            url=url,
            post_url=settings.POST_URL))

def main():
    run_client(TenyksLinkScraper)

if __name__ == '__main__':
    main()
