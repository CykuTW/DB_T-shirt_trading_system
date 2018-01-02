## Development Tips

1. Use Github flow
2. Use Angular commit style
3. **Do not** modify default_config.py, overwrite variable in config.py
4. Add config.py into `.git/info/exclude` and run `git update-index --assume-unchanged config.py`

## Development Environment

### Set up your MariaDB/MySQL and Redis server

```python
# in config.py
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/db?charset=utf8mb4'
REDIS_URL = 'redis://:@localhost:6379/0'
```

### Create environment (python virtual environment)

```bash
python -m venv venv # create a virtual environment folder called venv

# activate it
source venv/bin/activate # for Linux
venv\Scripts\activate # for Windows

# install required packages
pip install -r requirements.txt
```

### Initialize database (default use MySQL at localhost)

```bash
# initalize all tables
python app.py initdb
# create some test data
python app.py create_testdata
```

### Run the debug web server

```bash
python app.py run --host 0.0.0.0 --port 8000
```

## Architecture
檔案/目錄|說明
------------------|-------------------
app.py            | 程式入口點
default_config.py | server 預設設定
config.py         | server 自訂設定
models.py         | models (ORM物件)
utils.py          | 常用、通用函式
templates/        | 樣板檔案 (html files)
validators/       | 作 request 參數驗證的物件
views/            | 視圖函式 (Controller)
static/           | 靜態文件 (js、css、imgae files)
test/             | 所有單元測試、測試檔案均放在此處
flask_validate/   | 自訂的 extension，使用方法參閱下方

## flask_validate extension

1. 建立含有 validate method 的 validator class，將驗證邏輯寫入 validate method

```python
from flask import request


class SampleValidator(object):

    def validate(self) -> bool:
        keyword = request.args.get('keyword')
        return keyword and type(keyword) is str:
```

2. 在欲驗證的視圖函式 (view) 前方加入 validate decorator

```python
from flask.views import MethodView
from flask_validate import validate


# with function style
@app.route('/', ['GET'])
@validate(SampleValidator)
def index_view():
    return 'Home page needs keyword argument.'

# with object style
class IndexView(MethodView):

    @validate(SampleValidator)
    def get(self):
        return 'Home page needs keyword argument.'

app.add_url_rule('/', view_func=IndexView.as_view(IndexView.__name__))
```

3. flask_validate 驗證失敗會呼叫 flask.abort(400)，可用 error handler 覆寫錯誤訊息

```python
@app.errorhandler(400)
def error_handler(e):
    return '缺少必要的參數', 400
```

## Utilities (utils.py)

### generate_token(token_name=None) -> Union[str, str]
產生 CSRF 防禦用的 token，回傳 token_name 與 token，token_name 會影響儲存在 session 中的名稱，預設為 "token"。回傳的 token 則是該 token 的值，需手動在樣板 (template) 中插入。

### verify_token(token, token_name=None) -> bool
驗證 token 的函式，會去 session 中尋找與 token_name 相同的參數值並將其提出與傳入的 token 進行比較。token_name 預設為 "token"。

**token 預設 1 小時會過期，過期則須重新產生**

### is_safe_url(target) -> bool:  
驗證 url 字串是否安全 (是否屬於相同網域之中)。
