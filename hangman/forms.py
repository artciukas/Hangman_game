from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField, BooleanField, StringField, PasswordField, FloatField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from hangman.models import User



class RegisterForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    email = StringField('Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    verified_password = PasswordField("Repeat password", [EqualTo('password', "The password must match.")])
    submit = SubmitField('Login')

    def validate_name(self, name):
        user = User.query.filter_by(name=name.data).first()
        if user:
            raise ValidationError('This name has been used. Choose another.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email has been used. Choose another.')




class LoginForm(FlaskForm):
    email = StringField('Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField('Login')


class AccountUpdateForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    email = StringField('Email', [DataRequired()])
    photo = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    # def validate_name(self, name):
    #     if name.data != app.current_user.name:
    #         user = app.db.session.query(User).filter_by(name=name.data).first()
    #         if user:
    #             raise ValidationError('Šis name panaudotas. Pasirinkite kitą.')

    # def validate_email(self, email):
    #     if email.data != app.current_user.email:
    #         user = app.db.session.query(User).filter_by(email=email.data).first()
    #         if user:
    #             raise ValidationError('Šis el. pašto adresas panaudotas. Pasirinkite kitą.')
            
            
class StatisticsForm(FlaskForm):
    pajamos = BooleanField('Win')
    suma = FloatField('Defeat', [DataRequired()])
    submit = SubmitField('Įvesti')