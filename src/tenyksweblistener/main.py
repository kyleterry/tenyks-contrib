from flask import Flask
from tenyksservice import TenyksService, run_service

from .routes import app as routes


class TenyksWebListener(TenyksService):

    def run(self):
        app = Flask(__name__)
        app.register_blueprint(routes)
        app.run(host='0.0.0.0')


def main():
    run_service(TenyksWebListener)


if __name__=='__main__':
    main()
