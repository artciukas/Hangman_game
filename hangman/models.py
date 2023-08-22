
from sqlalchemy import DateTime
from flask_login import UserMixin
from datetime import datetime
from hangman import db, app


class Vartotojas(db.Model, UserMixin):
    __tablename__ = "vartotojas"
    id = db.Column(db.Integer, primary_key=True)
    vardas = db.Column("Name", db.String(20), unique=True, nullable=False)
    el_pastas = db.Column("Email", db.String(120), unique=True, nullable=False)
    nuotrauka = db.Column(db.String(20), nullable=False, default='default.jpg')
    slaptazodis = db.Column("Password", db.String(60), unique=True, nullable=False)


class Irasas(db.Model):
    __tablename__ = "irasas"
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column("Date", DateTime, default=datetime.now())
    laimejo = db.Column("Win", db.Integer)
    pralaimejo = db.Column("Defeat", db.Integer)
    vartotojas_id = db.Column(db.Integer, db.ForeignKey("vartotojas.id"))
    vartotojas = db.relationship("Vartotojas", lazy=True)

with app.app_context():
    db.create_all()