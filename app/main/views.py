from flask import flash, redirect, render_template, session, url_for, request
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from app import db
from app.decorators import admin_required, permission_required, mod_required
from app.main.forms import (
    EditProfileAdminForm, EditProfileForm, RoleForm, AgendaForm, PostForm
)
from app.models import Role, User, Agenda, Permission, Post, Follow

from . import main


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.has_permission(Permission.WRITE) and form.validate_on_submit():
        post = Post(
            body=form.body.data, author=current_user._get_current_object()
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(
        Post.timestamp.desc()
    ).paginate(
        page, per_page=10, error_out=False  
    )
    posts = pagination.items
    return render_template('index.html', form=form, posts=posts, pagination=pagination)

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@main.route('/voluntarios')
def voluntarios_list():
    profiles = User.query.all()
    return render_template('voluntarios.html', profiles=profiles)

@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return 'User invalid'
    follows = user.followers.all()
    return render_template('followers.html', username=username, followers=follows)


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid User')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('Você está seguindo %s' % username)
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    flash('Agora você está seguindo %s' % username)
    return redirect(url_for('.user', username=username))

@main.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Usuário %s não encontrado.'% username)
        return redirect(url_for('.index'))
    if user == current_user:
        flash('Função não realizada!')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('Você deixou de seguir %s' % username)
    return redirect(url_for('.user', username=username))

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Perfil editado com sucesso!')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.about_me.data = current_user.about_me
    return render_template(
        'edit_user.html', form=form, username=current_user.username)

@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('Usuário editado com sucesso!')
        return redirect(url_for('.edit_voluntarios_admin'))
    form.username.data = user.username
    form.role.data = user.role_id
    form.name.data = user.name
    form.about_me.data = user.about_me
    return render_template(
        'edit_profile.html', form=form, username=user.username
    )

@main.route('/criar-agenda', methods=['GET', 'POST'])
@login_required
@mod_required
def agenda():
    form = AgendaForm()
    agendar = Agenda.query.all()
    if form.validate_on_submit():
        new_agenda = Agenda()
        new_agenda.name_event = form.name_event.data
        new_agenda.date = form.date.data
        new_agenda.local = form.local.data
        new_agenda.description = form.description.data
        db.session.add(new_agenda)
        db.session.commit()
        flash('Evento cadastrado com sucesso!')
        return redirect(url_for('main.index'))
    return render_template('add_agenda.html', form=form)

@main.route('/agenda')
def agendas_list():
    eventos = Agenda.query.all()
    return render_template('agenda.html', eventos=eventos)

@main.route('/agenda/deleta-evento/<int:id>')
@login_required
@mod_required
def evento_delete():
    evento = Agenda.query.get_or_404(id)
    db.session.delete(evento)
    db.session.commit()
    return render_template('agenda.html', eventos=eventos)

@main.route('/administracao/lista-voluntarios')
@login_required
@admin_required
def edit_voluntarios_admin():
    profiles = User.query.all()
    return render_template('voluntarios_list.html', profiles=profiles)

@main.route('/administracao/deleta-voluntario/<int:id>')
@login_required
@admin_required
def deleta_voluntarios_admin(id):
    user = User.query.get_or_404(id)
    if user is not current_user:
        db.session.delete(user)
        db.session.commit()
    return render_template('voluntarios_list.html')