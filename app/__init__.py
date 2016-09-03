from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CsrfProtect


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
lm = LoginManager(app)
csrf = CsrfProtect(app)
lm.login_view = 'UserLogin'
import common
import users

@app.context_processor
def inject_permssions():
    return dict(Permssion=users.models.Permssion)

if __name__ == '__main__':
    app.run()