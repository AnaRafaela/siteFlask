from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, SelectField,\
    TextAreaField, DateField
from wtforms.validators import DataRequired, Length

from app.models import Role, User

class PostForm(FlaskForm):
    body = TextAreaField(
        'O que você está pensando?',
        validators=[DataRequired()]
    )
    submit = SubmitField('Enviar')

class EditProfileForm(FlaskForm):
    name = StringField('Nome completo', validators=[Length(1, 64)])
    location = StringField('Adicionar localização', validators=[Length(0, 64)])
    about_me = TextAreaField('Sobre mim')
    submit = SubmitField('Enviar')


class EditProfileAdminForm(FlaskForm):
    username = StringField('Usuário', validators=[
        DataRequired(), Length(1, 64)
    ])
    role = SelectField('Função', coerce=int)
    name = StringField('Nome completo', validators=[
        Length(1, 64)
    ])
    about_me = TextAreaField('Sobre mim')
    submit = SubmitField('Enviar')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [
            (role.id, role.name)
            for role in Role.query.order_by(Role.name).all()
        ]
        self.user = user

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Usuário já existe!')

class RoleForm(FlaskForm):
    name = StringField('Função', validators=[
        DataRequired()
    ])
    submit = SubmitField('Cadastrar')

    def validate_name(self, field):
        role = Role.query.filter_by(name=field.data).first()
        if role:
            raise ValidationError('Função já cadastrada')

class AgendaForm(FlaskForm):
    name_event = StringField('Nome do evento', validators=[Length(1, 64)])
    date = StringField('Data do evento')
    local = StringField('Adicionar localização', validators=[Length(0, 64)])
    description = TextAreaField('Descrição do evento...')
    submit = SubmitField('Cadastrar')