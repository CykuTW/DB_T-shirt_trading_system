from flask import Flask
from flask.cli import FlaskGroup


app = Flask(__name__)


def create_app(info=None):
    return app


cli = FlaskGroup(create_app=create_app)

if __name__ == '__main__':
    cli()
