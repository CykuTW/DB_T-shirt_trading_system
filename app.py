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
app.use_reloader = False
models.db.init_app(app)
utils.bcrypt.init_app(app)
utils.login_manager.init_app(app)
utils.redis_store.init_app(app)


# Set up login_manager
utils.login_manager.login_view = 'membership.LoginView'

@utils.login_manager.user_loader
def load_user(user_id):
    return models.Member.query.filter_by(id=user_id).first()


# Register blueprints
app.register_blueprint(views.membership.blueprint, url_prefix='/membership')
app.register_blueprint(views.goods.blueprint, url_prefix='/goods')
app.register_blueprint(views.shopping_cart.blueprint, url_prefix='/shopping_cart')
app.register_blueprint(views.shopping_cart.api_blueprint, url_prefix='/api/shopping_cart')


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

        goods_type = models.GoodsType()
        goods_type.size = 'M'
        goods_type.state = 'test'
        goods_type.price = 399
        models.db.session.add(goods_type)
        models.db.session.commit()

        goods = models.Goods()
        goods.name = 'test1'
        goods.state = 'test1'
        goods.type = goods_type
        goods.author = member
        goods.description = '''this is a description for test1.
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
        models.db.session.add(goods)
        models.db.session.commit()

        goods = models.Goods()
        goods.name = 'test2'
        goods.state = 'test2'
        goods.type = goods_type
        goods.author = member
        models.db.session.add(goods)
        models.db.session.commit()

        order = models.Order()
        order.amount = 399
        order.purchaser = member
        models.db.session.add(order)
        models.db.session.commit()

        order_item = models.OrderItem()
        order_item.quantity = 1
        order_item.goods = goods
        order_item.order = order
        models.db.session.add(order_item)
        models.db.session.commit()

        rating = models.Rating()
        rating.score = 4
        rating.message = 'hi'
        rating.for_order_item = order_item
        rating.author = member
        models.db.session.add(rating)
        models.db.session.commit()

        print(order_item.rating)


if __name__ == '__main__':
    cli()
