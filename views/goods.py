import models
from flask import Blueprint, request, abort, render_template
from flask.views import MethodView


blueprint = Blueprint('goods', __name__)


class GoodsView(MethodView):

    def get(self):
        good_type = request.args.get('type')
        keyword = request.args.get('keyword')
        page = request.args.get('page')
        count = request.args.get('count')

        query = models.Goods.query

        if good_type:
            query = query.join(models.GoodType).filter_by(size=good_type)
        
        if keyword:
            query = query.filter(models.Goods.name.like('%{}%'.format(keyword)))

        if page and count:
            query = query.limit(count).offset(count*(page-1))

        goods_list = query.all()
        return render_template('goods/index.html', goods_list=goods_list, args=request.args)


class GoodDetailView(MethodView):

    def get(self, good_id):
        goods = models.Goods.query \
                     .filter_by(id=good_id) \
                     .first() or abort(400)
        ratings = models.Rating.query \
                        .join(models.OrderItem) \
                        .filter_by(goods=goods).all()
        return render_template('goods/detail.html', goods=goods, ratings=ratings)


blueprint.add_url_rule('/', view_func=GoodsView.as_view(GoodsView.__name__))
blueprint.add_url_rule('/<int:good_id>', view_func=GoodDetailView.as_view(GoodDetailView.__name__))
