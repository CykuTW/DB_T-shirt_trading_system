import models
import utils
import validators
from flask import Blueprint, request, abort, redirect, render_template
from flask.views import MethodView
from flask_login import login_user, logout_user, current_user, login_required
from flask_validate import validate
from utils import bcrypt


blueprint = Blueprint('membership', __name__)


class LoginView(MethodView):

    def get(self):
        return render_template('membership/login.html')

    @validate(validators.membership.LoginValidator)
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
        if user.is_authenticated:
            return 'profile'
        return ''


class RegisterView(MethodView):

    def get(self):
        token = utils.generate_token()
        session['token'] = token
        return render_template('membership/register.html', token=token)

    @validate(validators.membership.RegisterValidator)
    def post(self):
        pass


class LogoutView(MethodView):

    def get(self):
        return self.post()

    def post(self):
        logout_user()
        return 'success'


blueprint.add_url_rule('/login', view_func=LoginView.as_view(LoginView.__name__))
blueprint.add_url_rule('/profile', view_func=ProfileView.as_view(ProfileView.__name__))
blueprint.add_url_rule('/register', view_func=RegisterView.as_view(RegisterView.__name__))
blueprint.add_url_rule('/logout', view_func=LogoutView.as_view(LogoutView.__name__))
