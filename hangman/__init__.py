import os
from flask_admin import Admin
from flask_login import current_user, LoginManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt





basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = '4654f5dfadsrfasdr54e6rae'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
admin = Admin(app)
db = SQLAlchemy(app)


bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'prisijungti'
# login_manager.login_message_category = 'info'
# login_manager.login_message = 'ka cia issidirbineji'
# print(f'aaaa{__name__}')


from hangman.models import Vartotojas

@login_manager.user_loader
def load_user(user_id: str) -> Vartotojas:
    return Vartotojas.query.get(int(user_id))

