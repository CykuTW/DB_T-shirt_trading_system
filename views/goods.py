import models
import validators
from flask import Blueprint, request, abort, render_template
from flask.views import MethodView
from flask_validate import validate


blueprint = Blueprint('goods', __name__)


class GoodsView(MethodView):

    @validate(validators.goods.SearchValidator)
    def get(self):
        good_type = request.args.get('type')
        keyword = request.args.get('keyword')
        page = request.args.get('page', 1)
        count = request.args.get('count', 12)

        query = models.Goods.query

        if good_type:
            query = query.join(models.GoodsType).filter_by(size=good_type)
        
        if keyword:
            query = query.filter(models.Goods.name.like('%{}%'.format(keyword)))

        query = query.limit(count).offset(count*(page-1))

        goods_list = query.all()
        goods_total = models.Goods.query.count()
        return render_template('goods/index.html', 
                               goods_list=goods_list,
                               goods_total=goods_total,
                               args=request.args)


class GoodsDetailView(MethodView):

    def get(self, goods_id):
        goods = models.Goods.query \
                     .filter_by(id=goods_id) \
                     .first() or abort(400)
        ratings = models.Rating.query \
                        .join(models.OrderItem) \
                        .filter_by(goods=goods).all()
        return render_template('goods/detail.html', goods=goods, ratings=ratings)


blueprint.add_url_rule('/', view_func=GoodsView.as_view(GoodsView.__name__))
blueprint.add_url_rule('/<int:goods_id>', view_func=GoodsDetailView.as_view(GoodsDetailView.__name__))
