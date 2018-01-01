import models
import utils
import pickle
import validators
from flask import Blueprint, request, abort, render_template, redirect, url_for
from flask.views import MethodView
from flask_login import current_user, login_required
from flask_validate import validate


blueprint = Blueprint('order', __name__)


class OrderView(MethodView):

    @login_required
    def get(self):
        user = current_user
        _items = utils.redis_store.smembers('_{}'.format(user.id))
        _items = [pickle.loads(i) for i in _items]
        items = []
        for item in _items:
            goods = models.Goods.query.filter_by(id=item['id']).first()
            if goods:
                items.append(goods)
        token_name, token = utils.generate_token()
        return render_template('/order/index.html', items=items, token=token)

    @login_required
    @validate(validators.order.NewOrder)
    def post(self):
        token = request.form.get('token')
        if not utils.verify_token(token):
            abort(401)

        user = current_user
        goods_list = request.form.getlist('goods[]')
        goods_quantity_list = request.form.getlist('goods_quantity[]')

        order = models.Order()
        order.is_paid = False
        order.amount = 0
        order.purchaser = user
        models.db.session.add(order)
        for index, goods_id in enumerate(goods_list):
            goods = models.Goods.query.filter_by(id=int(goods_id)).first()
            if goods:
                order_item = models.OrderItem()
                order_item.quantity = int(goods_quantity_list[index])
                order_item.goods = goods
                order_item.order = order
                order.amount += goods.type.price * order_item.quantity
                utils.redis_store.srem(
                    '_{}'.format(user.id),
                    pickle.dumps({
                        'id': goods.id,
                        'name': goods.name,
                        'size': goods.type.size,
                        'price': goods.type.price
                    })
                )
                models.db.session.add(order_item)
        models.db.session.commit()
        return redirect(url_for('order.OrderDetailView', order_id=order.id))


class OrderReadyView(MethodView):

    @login_required
    @validate(validators.order.NewOrder)
    def post(self):
        token = request.form.get('token')
        if not utils.verify_token(token):
            abort(401)

        user = current_user
        _goods_list = request.form.getlist('goods[]')
        goods_quantity_list = request.form.getlist('goods_quantity[]')
        goods_list = []
        amount = 0
        for index, goods_id in enumerate(_goods_list):
            goods = models.Goods.query.filter_by(id=goods_id).first()
            if goods and goods.state == 'to sell':
                goods_list.append(goods)
                amount += int(goods.type.price) * int(goods_quantity_list[index])
        token_name, token = utils.generate_token()
        return render_template('/order/ready.html',
                               goods_list=goods_list,
                               goods_quantity_list=goods_quantity_list,
                               amount=amount,
                               token=token
        )


class OrderListView(MethodView):

    def get(self):
        user = current_user
        order_list = models.Order.query.filter_by(purchaser=user).all()
        return render_template('/order/list.html', order_list=order_list)


class OrderDetailView(MethodView):

    def get(self, order_id):
        user = current_user
        order = models.Order.query.filter_by(id=order_id, purchaser=user).first()
        if not order:
            abort(404)
        return render_template('/order/detail.html', order=order)


blueprint.add_url_rule('/', view_func=OrderView.as_view(OrderView.__name__))
blueprint.add_url_rule('/ready', view_func=OrderReadyView.as_view(OrderReadyView.__name__))
blueprint.add_url_rule('/list', view_func=OrderListView.as_view(OrderListView.__name__))
blueprint.add_url_rule('/<int:order_id>', view_func=OrderDetailView.as_view(OrderDetailView.__name__))
