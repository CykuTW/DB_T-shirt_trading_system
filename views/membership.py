import models
from flask import Blueprint, request, render_template, session
from flask.views import MethodView
from utils import bcrypt


blueprint = Blueprint('membership', __name__)


class LoginView(MethodView):

    def get(self):
        return render_template('membership/login.html')

    def post(self):
        username = request.form['username']
        password = request.form['password']
        user = models.Member.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['id'] = user.id
            session['username'] = user.username
            return 'success'
        return 'fail'


class ProfileView(MethodView):

    def get(self):
        if session['username']:
            return 'profile'
        return ''


class LogoutView(MethodView):

    def post(self):
        session.clear()
        return 'success'


blueprint.add_url_rule('/login', view_func=LoginView.as_view(LoginView.__name__))
blueprint.add_url_rule('/profile', view_func=ProfileView.as_view(ProfileView.__name__))
blueprint.add_url_rule('/logout', view_func=LogoutView.as_view(LogoutView.__name__))
