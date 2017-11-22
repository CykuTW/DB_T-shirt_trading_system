import config
import models
import views
import utils
import click
import utils
from flask import Flask
from flask.cli import FlaskGroup


app = Flask(__name__)
app.config.from_object(config)
models.db.init_app(app)
utils.bcrypt.init_app(app)


# Register blueprints
app.register_blueprint(views.membership.blueprint, url_prefix='/membership')


def create_app(info=None):
    return app


cli = FlaskGroup(create_app=create_app)


@cli.command()
def initdb():
    click.echo('Initialize the database.')
    with app.app_context():
        models.db.drop_all()
        models.db.create_all()


@cli.command()
def create_testdata():
    click.echo('Create test data.')
    with app.app_context():
        member = models.Member()
        member.realname = '王小明'
        member.username = 'user'
        member.password = utils.bcrypt.generate_password_hash('password')
        member.email = 'xiaoming@gmail.com'
        member.sex = 'Male'
        member.phone = '0123456789'
        member.permission = 0x1
        models.db.session.add(member)
        models.db.session.commit()


if __name__ == '__main__':
    cli()
