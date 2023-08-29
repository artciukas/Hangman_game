import os
import logging
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
logging.basicConfig(level=logging.INFO,filename='logging_data.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'prisijungti'


from hangman.models import User

@login_manager.user_loader
def load_user(user_id: str) -> User:
    return User.query.get(int(user_id))

