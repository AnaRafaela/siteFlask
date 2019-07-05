from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from app.auth.forms import RegistrationForm
from app.models import User
from app import db

from . import auth
from .forms import LoginForm, RegistrationForm


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Usuário registrado!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Username ou senha inválida.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você não está mais logado.')
    return redirect(url_for('main.index'))
