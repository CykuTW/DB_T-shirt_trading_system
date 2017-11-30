import models
from flask import Blueprint, request, abort, render_template


blueprint = Blueprint('goods', __name__)


class GoodsView(MethodView):

    def get(self):
        good_type = request.form.get('type')
        keyword = request.form.get('keyword')
        page = request.form.get('page')
        count = request.form.get('count')

        query = models.Good.query

        if good_type:
            query = query.join(models.GoodType).filter_by(models.GoodType=good_type)
        
        if keyword:
            query = query.filter(models.Good.name.like('%{}%'.format(keyword)))

        if page and count:
            query = query.limit(count).offset(count*(page-1))

        goods = query.all()
        return render_template('goods/index.html', goods=goods)

blueprint.add_url_rule('/goods', view_func=GoodsView.as_view(GoodsView.__name__))