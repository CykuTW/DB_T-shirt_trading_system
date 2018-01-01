from flask import request
from wtforms import Form, StringField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, AnyOf, Regexp, InputRequired


class LoginValidator(object):
    class InnerValidator(Form):
        username = StringField('username', validators=[DataRequired(), Length(1, 20)])
        password = StringField('password', validators=[DataRequired(), Length(1, 1024)])

    def validate(self):
        validator = LoginValidator.InnerValidator(request.form)
        return validator.validate()


class RegisterValidator(object):
    class InnerValidator(Form):
        username = StringField('username', validators=[DataRequired(), Length(1, 20)])
        realname = StringField('realname', validators=[DataRequired(), Length(1, 50)])
        password = StringField('password', validators=[DataRequired(), Length(1, 1024)])
        confirm_password = StringField('confirm_password', validators=[DataRequired(), Length(1, 1024), EqualTo('password')])
        email = StringField('email', validators=[DataRequired(), Length(1, 256), Email()])
        sex = StringField('sex', validators=[DataRequired(), AnyOf(['male', 'female', 'others'])])
        birthday = DateTimeField('birthday', format=r'%Y-%m-%d', validators=[DataRequired()])
        phone = StringField('phone', validators=[DataRequired(), Length(1, 15), Regexp(r'^[\d\-]+$')])

    def validate(self):
        validator = RegisterValidator.InnerValidator(request.form)
        return validator.validate()


class ProfileValidator(object):
    class InnerValidator(Form):
        realname = StringField('realname', validators=[DataRequired(), Length(1, 50)])
        email = StringField('email', validators=[DataRequired(), Length(1, 256), Email()])
        sex = StringField('sex', validators=[DataRequired(), AnyOf(['male', 'female', 'others'])])
        birthday = DateTimeField('birthday', format=r'%Y-%m-%d', validators=[DataRequired()])
        phone = StringField('phone', validators=[DataRequired(), Length(1, 15), Regexp(r'^[\d\-]+$')])
        old_password = StringField('old_password', validators=[DataRequired(), Length(1, 1024)])
        new_password = StringField('new_password', validators=[InputRequired(), Length(1, 1024)])
        confirm_new_password = StringField('confirm_new_password', validators=[InputRequired(), Length(1, 1024), EqualTo('new_password')])

    def validate(self):
        validator = RegisterValidator.InnerValidator(request.form)
        return True #validator.validate()
