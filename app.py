import os
import config
import models
import views
import utils
import click
import utils
from flask import Flask, url_for, render_template
from flask.cli import FlaskGroup


app = Flask(__name__, static_url_path='/static')
app.config.from_object(config)
models.db.init_app(app)
utils.bcrypt.init_app(app)
utils.login_manager.init_app(app)


# Set up login_manager

utils.login_manager.login_view = 'membership.LoginView'

@utils.login_manager.user_loader
def load_user(user_id):
    return models.Member.query.filter_by(id=user_id).first()


# Register blueprints
app.register_blueprint(views.membership.blueprint, url_prefix='/membership')
app.register_blueprint(views.goods.blueprint, url_prefix='/goods')


# Error handler
@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(404)
@app.errorhandler(500)
@app.errorhandler(501)
def error_handler(e):
    error_file = os.path.join(os.getcwd(), 'templates/errors/{}.html'.format(e.code))
    if os.path.isfile(error_file):
        return render_template('errors/{}.html'.format(e.code)), e.code
    else:
        return str(e.code), e.code


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

        good_type = models.GoodType()
        good_type.size = 'M'
        good_type.state = 'test'
        good_type.price = 399
        models.db.session.add(good_type)
        models.db.session.commit()

        good = models.Good()
        good.name = 'test1'
        good.state = 'test1'
        good.type = good_type
        good.author = member
        good.description = '''this is a description for test1.
this is a description for test1.
this is a description for test1.
this is a description for test1.
this is a description for test1.
this is a description for test1.
this is a description for test1.
this is a description for test1.
this is a description for test1.
this is a description for test1.
this is a description for test1.
'''
        models.db.session.add(good)
        models.db.session.commit()

        good = models.Good()
        good.name = 'test2'
        good.state = 'test2'
        good.type = good_type
        good.author = member
        models.db.session.add(good)
        models.db.session.commit()


if __name__ == '__main__':
    cli()
