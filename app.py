import config
import models
from flask import Flask
from flask.cli import FlaskGroup


app = Flask(__name__)
app.config.from_object(config)
models.db.init_app(app)


def create_app(info=None):
    return app


cli = FlaskGroup(create_app=create_app)

if __name__ == '__main__':
    cli()
