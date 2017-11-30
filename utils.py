import string
import random
import models
import datetime
from flask import request, session
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from Crypto.Hash import SHA256
from urllib.parse import urlparse, urljoin


bcrypt = Bcrypt()

login_manager = LoginManager()

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


def generate_token(token_name=None):
    seq = string.ascii_letters + string.digits
    token = request.remote_addr + ''.join(random.choices(seq, k=30))
    h = SHA256.new()
    h.update(token.encode('UTF-8'))
    token = h.hexdigest()
    if not token_name:
        token_name = 'token'
    session[token_name] = token
    session[token_name + '_expired'] = datetime.timedelta(hours=1).total_seconds()
    session[token_name + '_generated_time'] = datetime.datetime.now().timestamp()
    return token_name, token

def verify_token(token, token_name=None):
    if not token_name:
        token_name = 'token'
    expired = datetime.timedelta(seconds=session[token_name + '_expired'])
    generate_time = datetime.datetime.fromtimestamp(session[token_name + '_generated_time'])
    return token and \
            token == session[token_name] and \
            datetime.datetime.now() <= generate_time + expired