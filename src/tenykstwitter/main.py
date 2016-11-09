import re
import requests
from bs4 import BeautifulSoup
from tenyksservice import TenyksService, run_service, FilterChain

class TenyksTwitter(TenyksService):
    direct_only = False
    irc_message_filters = {
            'tweet': FilterChain([r'((https?)://(www\.)?twitter\.com/[^.\s]+/[^.\s]+)']),
    }

    def __init__(self, name, settings):
        super(TenyksTwitter, self).__init__(name, settings)

    def handle_tweet(self, data, match):
        url = match.group(1)

        req = requests.get(url)
        soup = BeautifulSoup(req.text, "html.parser")
        result = soup.title.text.split("Twitter: ")[1].replace('"', "")
        urls = re.findall('http[s]?://t.co/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', result)

        for url in urls:
            head = requests.head(url)
            actual_url = head.headers["location"]
            images = re.findall('(http[s]?://twitter.com/([a-zA-Z]|[0-9]|[$-_@.&+])+/status/[0-9]+/photo/([0-9])+)', actual_url)
            if images:
                result = result.replace(url, "")
                image_req = requests.get(images[0][0])
                soup2 = BeautifulSoup(image_req.text, "html.parser")
                imgs = soup2.findAll("div", {"class": "AdaptiveMedia-photoContainer js-adaptive-photo "})

                tweet_images = []
                for img in imgs:
                    tweet_images.append(img.img.attrs["src"])
                result = "{}{}".format(result, " ".join(tweet_images))
            else:
                result = result.replace(url, actual_url)
        self.send("Tweet: {}".format(result), data)

def main():
    run_service(TenyksTwitter)

if __name__ == '__main__':
    main()
