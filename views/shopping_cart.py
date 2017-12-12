import utils
import models
import pickle
import blinker
from flask import Blueprint, request, abort, render_template, request_started
from flask.views import MethodView
from flask_login import login_required, current_user


blueprint = Blueprint('shopping_cart', __name__)


class ShoppingCartView(MethodView):

    @login_required
    def get(self):
        user = current_user
        items = utils.redis_store.smembers('_{}'.format(user.id))
        items = [pickle.loads(i) for i in items]
        return render_template('/shopping_cart/index.html', items=items)

    @login_required
    def post(self):
        good_id = request.form['good_id']
        good = models.Good.query.filter_by(id=good_id).first() or abort(400)
        user = current_user
        utils.redis_store.sadd(
            '_{}'.format(user.id), 
            pickle.dumps({
                'id': good.id,
                'name': good.name,
                'size': good.type.size,
                'price': good.type.price
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
            utils.redis_store.sadd(
                '_{}'.format(user.id),
                pickle.dumps(item.good)
            )


@request_started.connect_via(blinker.ANY) # ANY sender
def _register_signal_handler(sender, **extra):
    # Set up redis keyspace notification callback
    def _redis_del_key_handler(message):
        print('redis expire:', message.data)

    _pubsub = utils.redis_store.pubsub()
    _pubsub.psubscribe(**{
        '__keyevent@0__:expire': _redis_del_key_handler
    })
    _pubsub.run_in_thread(sleep_time=1)
    request_started.disconnect(_register_signal_handler)


blueprint.add_url_rule('/', view_func=ShoppingCartView.as_view(ShoppingCartView.__name__))
