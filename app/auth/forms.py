from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length

from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Usuário', validators=[
        DataRequired(), Length(1, 64)
    ])
    password = PasswordField('Senha', validators=[
        DataRequired()
    ])
    password2 = PasswordField('Confirmar Senha', validators=[
        DataRequired(), EqualTo('password', message='Senhas não conferem.')
    ])
    submit = SubmitField('Registrar')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Usuário já registrado.")


        
class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[
        DataRequired()
    ])
    password = PasswordField('Senha', validators=[
        DataRequired()
    ])
    remember_me = BooleanField('Manter logado')
    submit = SubmitField('Login')
