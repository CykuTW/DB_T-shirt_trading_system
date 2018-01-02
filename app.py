import os
import config
import models
import views
import utils
import click
import utils
from flask import Flask, url_for, render_template, escape, redirect
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
app.register_blueprint(views.order.blueprint, url_prefix='/order')
app.register_blueprint(views.shopping_cart.api_blueprint, url_prefix='/api/shopping_cart')


@app.route('/')
def home():
    return redirect(url_for('goods.GoodsView'))

# Error handler
@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(404)
@app.errorhandler(500)
@app.errorhandler(501)
def error_handler(e):
    error_file = os.path.join(os.getcwd(), 'templates/errors/{}.html'.format(e.code))
    if os.path.isfile(error_file):
        return render_template('errors/{}.html'.format(e.code), error=e), e.code
    else:
        return '{}, {}'.format(str(e.code), escape(e.description)), e.code


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
        member.sex = 'male'
        member.phone = '0123456789'
        member.permission = 0x1
        models.db.session.add(member)

        goods_type = models.GoodsType()
        goods_type.size = 'M'
        goods_type.state = 'test'
        goods_type.price = 399
        models.db.session.add(goods_type)

        goods = models.Goods()
        goods.name = 'Sad Frog'
        goods.state = 'to sell'
        goods.type = goods_type
        goods.author = member
        goods.image = '/static/images/pepe-the-frog-s.jpg'

        models.db.session.add(goods)

        goods = models.Goods()
        goods.name = 'Cool Frog'
        goods.state = 'to sell'
        goods.type = goods_type
        goods.author = member
        goods.description = '''this is a description for Cool Frog.
this is a description for Cool Frog.
this is a description for Cool Frog.
this is a description for Cool Frog.
this is a description for Cool Frog.
this is a description for Cool Frog.
this is a description for Cool Frog.
this is a description for Cool Frog.
this is a description for Cool Frog.
this is a description for Cool Frog.
this is a description for Cool Frog.
'''
        goods.image = '/static/images/pepe-cool-the-frog-s.jpg'
        models.db.session.add(goods)

        order = models.Order()
        order.amount = 399
        order.purchaser = member
        models.db.session.add(order)

        order_item = models.OrderItem()
        order_item.quantity = 1
        order_item.goods = goods
        order_item.order = order
        models.db.session.add(order_item)

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
