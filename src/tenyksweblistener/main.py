from flask import Flask
from tenyks.client import Client, run_client
from tenyks.client.config import settings

from .routes import app as routes


class TenyksWebListener(Client):

    def run(self):
        app = Flask(__name__)
        app.register_blueprint(routes)
        app.run(host='0.0.0.0')


def main():
    run_client(TenyksWebListener)


if __name__=='__main__':
    main()
