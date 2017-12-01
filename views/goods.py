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

        query = models.Good.query

        if good_type:
            query = query.join(models.GoodType).filter_by(size=good_type)
        
        if keyword:
            query = query.filter(models.Good.name.like('%{}%'.format(keyword)))

        if page and count:
            query = query.limit(count).offset(count*(page-1))

        goods = query.all()
        return render_template('goods/index.html', goods=goods, args=request.args)

blueprint.add_url_rule('/', view_func=GoodsView.as_view(GoodsView.__name__))