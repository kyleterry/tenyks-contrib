import unittest
from .. import hextime

class TestHexTimeScript(unittest.TestCase):

    def test_will_respond_with_hextime(self):
        data = {
            "payload": "current time in hex"
        }

        response = hextime.run(data, None)
        assert response
