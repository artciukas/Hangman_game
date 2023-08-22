from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField, BooleanField, StringField, PasswordField, FloatField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from hangman.models import Vartotojas



class RegistracijosForma(FlaskForm):
    vardas = StringField('Name', [DataRequired()])
    el_pastas = StringField('Email', [DataRequired()])
    slaptazodis = PasswordField('Password', [DataRequired()])
    patvirtintas_slaptazodis = PasswordField("Repeat password", [EqualTo('slaptazodis', "The password must match.")])
    submit = SubmitField('Login')

    def validate_vardas(self, vardas):
        vartotojas = Vartotojas.query.filter_by(vardas=vardas.data).first()
        if vartotojas:
            raise ValidationError('This name has been used. Choose another.')

    def validate_el_pastas(self, el_pastas):
        vartotojas = Vartotojas.query.filter_by(el_pastas=el_pastas.data).first()
        if vartotojas:
            raise ValidationError('This email has been used. Choose another.')




class PrisijungimoForma(FlaskForm):
    el_pastas = StringField('Email', [DataRequired()])
    slaptazodis = PasswordField('Password', [DataRequired()])
    prisiminti = BooleanField("Remember me")
    submit = SubmitField('Login')


class PaskyrosAtnaujinimoForma(FlaskForm):
    vardas = StringField('Name', [DataRequired()])
    el_pastas = StringField('Email', [DataRequired()])
    nuotrauka = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    # def validate_vardas(self, vardas):
    #     if vardas.data != app.current_user.vardas:
    #         vartotojas = app.db.session.query(Vartotojas).filter_by(vardas=vardas.data).first()
    #         if vartotojas:
    #             raise ValidationError('Šis vardas panaudotas. Pasirinkite kitą.')

    # def validate_el_pastas(self, el_pastas):
    #     if el_pastas.data != app.current_user.el_pastas:
    #         vartotojas = app.db.session.query(Vartotojas).filter_by(el_pastas=el_pastas.data).first()
    #         if vartotojas:
    #             raise ValidationError('Šis el. pašto adresas panaudotas. Pasirinkite kitą.')
            
            
# class IrasasForm(FlaskForm):
#     pajamos = BooleanField('Pajamos')
#     suma = FloatField('Suma', [DataRequired()])
#     submit = SubmitField('Įvesti')