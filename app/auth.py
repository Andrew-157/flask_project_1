from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from . import db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password1 = request.form['password1']
        remember = True if request.form.get('remember') else False
        errors = False

        # Check that user entered the necessary data
        if not username:
            flash('Username is required.')
            errors = True
        if not email:
            flash('Email is required.')
            errors = True
        if not password:
            flash('Password is required.')
            errors = True

        # Check that the entered data is not too long
        if len(username) > 50:
            flash('Username is too long.')
            errors = True
        if len(email) > 120:
            flash('Email is too long.')
            errors = True
        if len(password) > 200:
            flash('Password is too long.')
            errors = True

        # Check that passwords match
        if password != password1:
            flash('Passwords did not match')
            errors = True

        # Check that username is not too short
        if len(username) < 5:
            flash('Username is too short.')
            errors = True

        user_with_email = User.query.filter_by(email=email).first()
        user_with_username = User.query.filter_by(username=username).first()

        if user_with_email:
            flash('User with this email already exists.')
            errors = True
        if user_with_username:
            flash('User with this username already exists.')
            errors = True

        if errors:
            return redirect(url_for('auth.register'))

        new_user = User(username=username,
                        email=email,
                        password=generate_password_hash(password))

        db.session.add(new_user)
        db.session.commit()

        login_user(user=new_user, remember=remember)

        flash('You successfully registered to Asklee', category='success')

        return redirect(url_for('main.index'))

    return render_template('auth/register.html')


@bp.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember = True if request.form.get('remember') else False
        errors = False

        if not email:
            flash('Email is required to login.')
            errors = True
        if not password:
            flash('Password is required to login.')
            errors = True

        user = User.query.filter_by(email=email).first()

        if not user:
            flash('This email was not found.')
            errors = True
        if not check_password_hash(user.password, password):
            flash('Password does not match.')
            errors = True

        if errors:
            return redirect(url_for('auth.login'))

        login_user(user=user, remember=remember)
        flash('Welcome back to Asklee.', 'success')

        return redirect(url_for('main.index'))

    return render_template('auth/login.html')


@bp.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/change_profile/', methods=['GET', 'POST'])
@login_required
def change_profile():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        errors = False

        if not email:
            flash('Email is required.')
            errors = True
        if not username:
            flash('Username is required.')
            errors = True

        if len(email) > 120:
            flash('Email is too long.')
            errors = True
        if len(username) > 50:
            flash('Username is too long.')
            errors = True

        if len(username) < 5:
            flash('Username is too short.')
            errors = True

        user_with_email = User.query.filter_by(email=email).first()
        user_with_username = User.query.filter_by(username=username).first()

        if user_with_email and (user_with_email != current_user):
            flash('User with this email already exists.')
            errors = True
        if user_with_username and (user_with_username != current_user):
            flash('User with this username already exists.')
            errors = True

        if errors:
            return redirect(url_for('auth.change_profile'))

        current_user.username = username
        current_user.email = email
        db.session.commit()

        flash('You successfully updated your profile.', 'success')
        return redirect(url_for('main.index'))

    return render_template('auth/change_profile.html',
                           username=current_user.username,
                           email=current_user.email)
