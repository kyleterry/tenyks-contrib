import requests
from html.parser import HTMLParser
from bs4 import BeautifulSoup


def run(data, settings):
    if data['payload'] == 'urban dictionary me':
        req = requests.get('http://www.urbandictionary.com/random.php')

        soup = BeautifulSoup(req.text,
                             convertEntities=BeautifulSoup.HTML_ENTITIES)

        # The word is inner text of the child span of the td with class 'word'
        word = soup.findAll('td', attrs={'class': 'word'})[0].findChild().text

        # Definitions are just innertext of divs with class definition
        definition_divs = soup.findAll('div', attrs={'class': 'definition'})

        # BS doesn't unescape hex html encoded characaters, need HTMLParser
        parser = HTMLParser()
        definitions = [parser.unescape(div.text) for div in definition_divs]

        # Just use the first definition
        return '{0} - {1}'.format(word, definitions[0])
