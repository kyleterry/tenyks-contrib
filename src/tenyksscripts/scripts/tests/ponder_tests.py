from .. import ponder
import unittest
import os

class TestPonderScript(unittest.TestCase):

    def setUp(self):
        class FakeSettings(object):
            pass
        self.settings = FakeSettings()
        TEST_DIR = os.path.dirname(os.path.realpath(__file__))
        self.settings.PONDERINGS_FILE = TEST_DIR + '/test_ponderings.txt'
        with open(self.settings.PONDERINGS_FILE, 'w+') as f:
            pass

    def tearDown(self):
        os.remove(self.settings.PONDERINGS_FILE)

    def test_it_returns_a_url(self):
        data = {
            "payload": "give me a creepy url"
        }
        url = ponder.run(data, None)
        if not ponder.is_url(url):
            assert False, "Expected a URL, got {}".format(url)

    def test_it_ignores_other_payloads(self):
        data = {
            "payload": "give me a high five"
        }
        url = ponder.run(data, None)
        if url:
            assert False, "Expected None, got {}".format(url)

    def test_a_user_can_add_a_url(self):
        data = {
            'payload': 'add this creepy url http://google.com'
        }
        result = ponder.run(data, self.settings)
        assert result == 'Aight, I added it.', 'Failed to add URL, got: {}'.format(result)

        data = {
            'payload': 'give me a creepy url'
        }

        url = ponder.run(data, self.settings)
        assert url == 'http://google.com', 'Expected http://google.com, got: {}'.format(url)
