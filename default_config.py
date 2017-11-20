DEBUG = True
SECRET_KEY = '^Z7Q$hLsN#yTFqg%Rd&Vj4&6Vs?@vS'

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/test-db?charset=utf8mb4'
# <ENGINE>://<USER>:<PASSWORD>@<HOST>/<DB>?charset=<CHARACTER_SET>
SQLALCHEMY_TRACK_MODIFICATIONS = True

BCRYPT_HANDLE_LONG_PASSWORDS = True
