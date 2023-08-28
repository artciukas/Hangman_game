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

    def validate_name(self, name: str):
        user = User.query.filter_by(name=name.data).first()
        if user:
            raise ValidationError('This name has been used. Choose another.')

    def validate_email(self, email: str):
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
