import utils
import models
import pickle
from flask import Blueprint, request, abort, render_template
from flask.views import MethodView
from flask_login import login_required, current_user


blueprint = Blueprint('shopping_cart', __name__)


class ShoppingCartView(MethodView):

    def get(self):
        good = models.Good.query.filter_by(id=1).first() or abort(400)
        utils.redis_store.set('a', pickle.dumps(good))
        print(type(pickle.loads(utils.redis_store.get('a'))))
        return ''

    @login_required
    def post(self):
        good_id = request.form['good_id']
        good = models.Good.query.filter_by(id=good_id).first() or abort(400)
        user = current_user
        utils.redis_store.set(str(current_user.id), 1)
        utils.redis_store.lpush(
            '_{}'.format(current_user.id), 
            pickle.dumps(good)
        )


# Set up redis keyspace notification callback
def _redis_del_key_handler(message):
    print('redie expire:', message.data)

_pubsub = None
def init_app(app):
    global _pubsub
    _pubsub = utils.redis_store.pubsub()
    _pubsub.psubscribe(**{
        '__keyevent@0__:expire': _redis_del_key_handler
    })
    _pubsub.run_in_thread()

blueprint.add_url_rule('/', view_func=ShoppingCartView.as_view(ShoppingCartView.__name__))
