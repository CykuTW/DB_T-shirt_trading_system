from flask import request
from wtforms import Form, StringField
from wtforms.validators import DataRequired, Length


class LoginValidator(object):
    class InnerValidator(Form):
        username = StringField('username', validators=[DataRequired(), Length(1, 20)])
        password = StringField('password', validators=[DataRequired(), Length(1, 1024)])

    def validate(self):
        validator = Register.InnerValidator(request.form)
        return validator.validate()


class RegisterValidator(object):
    class InnerValidator(Form):
        username = StringField('username', validators=[DataRequired(), Length(1, 20)])
        realname = StringField('realname', validators=[DataRequired(), Length(1, 50)])

    def validate(self):
        validator = Register.InnerValidator(request.form)
        return validator.validate()
