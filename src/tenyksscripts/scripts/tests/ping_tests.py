import unittest
from .. import ping

class TestPingScript(unittest.TestCase):

    def test_will_respond_with_pong(self):
        data = {
            "payload": "ping"
        }

        response = ping.run(data, None)
        assert response == "pong"
