import models
import utils
from flask import Blueprint, request, abort, redirect, render_template
from flask.views import MethodView
from flask_login import login_user, logout_user, current_user, login_required
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
            login_user(user)
            next = request.args.get('next')
            if not next or not utils.is_safe_url(next):
                return redirect('/membership/profile')
            return redirect(next)
        return 'fail'


class ProfileView(MethodView):

    @login_required
    def get(self):
        user = current_user
        if user.is_authenticated():
            return 'profile'
        return ''


class LogoutView(MethodView):

    def get(self):
        return self.post()

    def post(self):
        logout_user()
        return 'success'


blueprint.add_url_rule('/login', view_func=LoginView.as_view(LoginView.__name__))
blueprint.add_url_rule('/profile', view_func=ProfileView.as_view(ProfileView.__name__))
blueprint.add_url_rule('/logout', view_func=LogoutView.as_view(LogoutView.__name__))
