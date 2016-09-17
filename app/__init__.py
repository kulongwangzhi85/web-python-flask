from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CsrfProtect
from flask_cache import Cache


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
lm = LoginManager(app)
csrf = CsrfProtect(app)
cache = Cache(app, config={'CACHE_TYPE': 'filesystem', 'CACHE_DIR': app.config['CACHE_DIR'], 'CACHE_DEFAULT_TIMEOUT':
    app.config['CACHE_DEFAULT_TIMEOUT']})
lm.login_view = 'UserLogin'
import common
import users

@app.context_processor
def inject_permssions():
    return dict(Permssion=users.models.Permssion)

if __name__ == '__main__':
    app.run()