from flask import flash, render_template,redirect, url_for, request
from apps.auth import bp
from apps.models import  User
from apps import db, login
from apps.auth.forms import RegisterForm, LoginForm
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('todo.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        if not form.username.data or not form.email.data or not form.password.data:
            flash('Must include username, email and password fields','danger') #this is flash message ('message', 'message category in bootstrap')
            return render_template('auth/register.html', form=form)
        if User.query.filter_by(username=form.username.data).first():
            flash('Please use a different username','danger')
            return render_template('auth/register.html', form=form)
        if User.query.filter_by(email=form.email.data).first():
            flash('Please use a different email address','danger')
            return render_template('auth/register.html', form=form)
        user = User(username=form.username.data,email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User registered!','success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('todo.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()        
        if user is None or not user.check_password(form.password.data):
            flash('Username or password invalid','danger')
            return redirect(url_for('auth.login'))        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('todo.index')
        return redirect(next_page)
    return render_template('auth/login.html',form=form)

@bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
