import string
import random
import models
from flask import request
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


def generate_token():
    seq = string.ascii_letters + string.digits
    token = request.remote_addr + ''.join(random.choices(seq, k=30))
    h = SHA256.new()
    h.update(token.encode('UTF-8'))
    token = h.hexdigest()
    return token
