
from sqlalchemy import DateTime
from flask_login import UserMixin
from datetime import datetime
from hangman import db, app


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column("Name", db.String(20), unique=True, nullable=False)
    email = db.Column("Email", db.String(120), unique=True, nullable=False)
    photo = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column("Password", db.String(60), unique=True, nullable=False)


class Statistics(db.Model):
    __tablename__ = "statistics"
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column("Date", DateTime, default=datetime.now())
    wins = db.Column("Win", db.Integer)
    defeats = db.Column("Defeat", db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", lazy=True)

    def __repr__(self) -> str:
        return f'{self.id}, {self.data}, {self.wins}, {self.defeats}'


with app.app_context():
    db.create_all()