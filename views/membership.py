import models
import utils
import validators
from flask import Blueprint, request, abort, redirect, render_template, session, abort, url_for
from flask.views import MethodView
from flask_login import login_user, logout_user, current_user, login_required
from flask_validate import validate
from utils import bcrypt


blueprint = Blueprint('membership', __name__)


class LoginView(MethodView):

    def get(self):
        token_name, token = utils.generate_token()
        return render_template('membership/login.html', token=token)

    @validate(validators.membership.LoginValidator)
    def post(self):
        token = request.form.get('token')
        if not utils.verify_token(token):
            abort(401)

        username = request.form['username']
        password = request.form['password']
        user = models.Member.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            next = request.args.get('next')
            if not next or not utils.is_safe_url(next):
                return redirect(url_for('membership.ProfileView'))
            return redirect(next)
        return 'fail'


class ProfileView(MethodView):

    @login_required
    def get(self):
        user = current_user
        token_name, token = utils.generate_token()
        return render_template('/membership/profile.html', user=user, token=token)

    @login_required
    @validate(validators.membership.ProfileValidator)
    def post(self):
        token = request.form.get('token')
        if not utils.verify_token(token):
            abort(401)

        realname = request.form.get('realname')
        email = request.form.get('email')
        sex = request.form.get('sex')
        birthday = request.form.get('birthday')
        phone = request.form.get('phone')
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')

        user = current_user
        if not bcrypt.check_password_hash(user.password, old_password):
            abort(400, '舊密碼輸入錯誤')

        user.realname = realname
        user.email = email
        user.sex = sex
        user.birthday = birthday
        user.phone = phone
        if new_password:
            user.pasword = bcrypt.generate_password_hash(new_password)
        models.db.session.commit()

        return redirect(url_for('membership.ProfileView'))


class RegisterView(MethodView):

    def get(self):
        token_name, token = utils.generate_token()
        return render_template('membership/register.html', token=token)

    @validate(validators.membership.RegisterValidator)
    def post(self):
        token = request.form.get('token')
        if not utils.verify_token(token):
            abort(401)

        username = request.form.get('username')
        realname = request.form.get('realname')
        email = request.form.get('email')
        sex = request.form.get('sex')
        birthday = request.form.get('birthday')
        phone = request.form.get('phone')
        password = request.form.get('password')

        user = models.Member.query.filter_by(username=username).first()
        # duplicate username
        if user:
            return '此帳戶名稱已被使用'

        user = models.Member()
        user.username = username
        user.realname = realname
        user.password = bcrypt.generate_password_hash(password)
        user.email = email
        user.sex = sex
        user.birthday = birthday
        user.phone = phone
        models.db.session.add(user)
        models.db.session.commit()
        return '註冊成功'


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
