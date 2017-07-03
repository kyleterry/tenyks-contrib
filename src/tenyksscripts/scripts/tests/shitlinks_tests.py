import unittest
import re
from .. import shitlinks


class TestShitLinksScript(unittest.TestCase):

    def test_random_bump_command(self):
        data = {
            "payload": "dank memes"
        }

        response = shitlinks.run(data, None)
        assert is_link(response)

    def test_invalid_command(self):
        data = {
            "payload": "i donno"
        }

        response = shitlinks.run(data, None)
        assert response is None

    def test_stats_command(self):
        data = {
            "payload": "shithouse stats"
        }

        response = shitlinks.run(data, None)
        assert not is_link(response) and response is not None

    def test_text_search_command(self):
        data = {
            "payload": "dank text don't tell anyone how i live"
        }

        response = shitlinks.run(data, None)
        assert is_link(response)

    def test_text_search_no_body_command(self):
        data = {
            "payload": "dank text"
        }

        response = shitlinks.run(data, None)
        assert not is_link(response)


def is_link(string):
    return re.compile('(.*)http:\/\/(.*)\.shithouse\.tv$').match(string)