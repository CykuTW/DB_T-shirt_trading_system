from flask import request
from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, AnyOf, DataRequired, NumberRange


class SearchValidator(object):
    def validate(self):
        try:
            int(request.args.get('page', 0))
            int(request.args.get('count', 0))
        except ValueError:
            return False

        goods_type = request.args.get('type') 
        if goods_type and goods_type not in ('S', 'M', 'L', 'XL', 'XXL'):
            return False

        return True
