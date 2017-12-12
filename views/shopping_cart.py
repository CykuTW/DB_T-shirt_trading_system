import utils
import models
import pickle
import blinker
from flask import Blueprint, request, abort, render_template, request_started, current_app
from flask.views import MethodView
from flask_login import login_required, current_user


blueprint = Blueprint('shopping_cart', __name__)
api_blueprint = Blueprint('api_shopping_cart', __name__)


class ShoppingCartView(MethodView):

    @login_required
    def get(self):
        user = current_user
        items = utils.redis_store.smembers('_{}'.format(user.id))
        items = [pickle.loads(i) for i in items]
        return render_template('/shopping_cart/index.html', items=items)


class ApiShoppingCartView(MethodView):

    @login_required
    def post(self):
        goods_id = request.form['goods_id']
        goods = models.Good.query.filter_by(id=good_id).first() or abort(400)
        user = current_user
        utils.redis_store.sadd(
            '_{}'.format(user.id), 
            pickle.dumps({
                'id': goods.id,
                'name': goods.name,
                'size': goods.type.size,
                'price': goods.type.price
            })
        )
        return 'OK'


class ApiShoppingCartItemView(MethodView):

    @login_required
    def delete(self, goods_id):
        user = current_user
        goods = models.Good.query.filter_by(id=goods_id).first() or abort(400)
        utils.redis_store.srem(
            '_{}'.format(user.id),
            pickle.dumps({
                'id': goods.id,
                'name': goods.name,
                'size': goods.type.size,
                'price': goods.type.price
            })
        )
        return 'OK'


@blueprint.before_request
@login_required
def _before_request():
    user = current_user
    if not utils.redis_store.get(str(user.id)):
        utils.redis_store.set(str(user.id), 1)
        utils.redis_store.expire(str(user.id), 60*60) # 1 hour
        utils.redis_store.delete('_{}'.format(user.id))
        for item in user.shopping_cart:
            goods = item.goods
            utils.redis_store.sadd(
                '_{}'.format(user.id),
                pickle.dumps({
                    'id': goods.id,
                    'name': goods.name,
                    'size': goods.type.size,
                    'price': goods.type.price
                })
            )
            models.db.session.delete(item)
            models.db.session.commit()


@request_started.connect_via(blinker.ANY) # ANY sender
def _register_signal_handler(sender, **extra):
    # Set up redis keyspace notification callback
    def _redis_expire_key_handler(message):
        from app import app
        with app.app_context():
            user_id = int(message['data'])
            user = models.Member.query.filter_by(id=user_id).first()
            if not user:
                return

            items = utils.redis_store.smembers('_{}'.format(user_id))
            items = [pickle.loads(i) for i in items]
            for item in items:
                goods = models.Good \
                            .query \
                            .filter_by(id=item['id']) \
                            .first()
                if not goods:
                    continue
                item = models.ShoppingCartItem()
                item.goods = goods
                item.member = user
                models.db.session.add(item)
            utils.redis_store.delete('_{}'.format(user_id))
            models.db.session.commit()

    _pubsub = utils.redis_store.pubsub()
    _pubsub.psubscribe(**{
        '__keyevent@0__:*': _redis_expire_key_handler
    })
    _pubsub.run_in_thread(sleep_time=1)
    request_started.disconnect(_register_signal_handler)


blueprint.add_url_rule('/', view_func=ShoppingCartView.as_view(ShoppingCartView.__name__))
api_blueprint.add_url_rule('/', view_func=ApiShoppingCartView.as_view(ApiShoppingCartView.__name__))
api_blueprint.add_url_rule('/<int:goods_id>', view_func=ApiShoppingCartItemView.as_view(ApiShoppingCartItemView.__name__))
