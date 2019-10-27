from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import func

from models.driver import Driver
from models.gameapp import Schedule, Track
from models.webapp import User
from webapp import app, db
from webapp.email import send_password_reset_email
from webapp.forms import LoginForm, RegistrationForm, reset_password_request_form, reset_password_form


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.setPassword(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return redirect(url_for('index'))

    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.checkPassword(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))

    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_passwordRequest():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = reset_password_request_form()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            send_password_reset_email(user)

        flash('Please check your email for the instructions to reset your password.')

        return redirect(url_for('login'))

    return render_template('reset_passwordRequest.html', title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    user = User.verify_reset_password_token(token)

    if not user:
        return redirect(url_for('index'))

    form = reset_password_form()

    if form.validate_on_submit():
        user.setPassword(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))

    return render_template('reset_password.html', form=form)


@app.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template('profile.html', user=user)


@app.route('/schedule')
def schedule():
    return render_template('schedule.html', schedule=Schedule.query.all(), trackDb=Track)


@app.route('/tracks')
@app.route('/tracks/<track_name>')
def tracks(track_name=None):
    if track_name is None:
        return render_template('trackList.html', tracks=Track.query.all())
    else:
        track_name = track_name.replace('-', ' ')
        track = Track.query.filter(func.lower(Track.name) == func.lower(track_name)).first()
        return render_template('trackInfo.html', track=track)


@app.route('/drivers')
def drivers():
    return render_template('drivers.html')


@app.route('/teams')
def teams():
    return render_template('teams.html')