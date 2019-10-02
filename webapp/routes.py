from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required

from models.driver import Driver
from models.gameapp import Schedule, Track
from models.webapp import User
from webapp import app, db
from webapp.email import sendPasswordResetEmail
from webapp.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm


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

        login_user(user, remember=form.rememberMe.data)
        return redirect(url_for('index'))

    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/resetPassword', methods=['GET', 'POST'])
def resetPasswordRequest():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = ResetPasswordRequestForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            sendPasswordResetEmail(user)

        flash('Please check your email for the instructions to reset your password.')

        return redirect(url_for('login'))

    return render_template('resetPasswordRequest.html', title='Reset Password', form=form)


@app.route('/resetPassword/<token>', methods=['GET', 'POST'])
def resetPassword(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    user = User.verifyResetPasswordToken(token)

    if not user:
        return redirect(url_for('index'))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        user.setPassword(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))

    return render_template('resetPassword.html', form=form)


@app.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template('profile.html', user=user)


@app.route('/schedule')
def schedule():
    return render_template('schedule.html', schedule=Schedule.query.all(), trackDb=Track)


@app.route('/tracks')
@app.route('/tracks/<trackId>')
def tracks(trackId=None):
    if trackId is None:
        return render_template('tracks.html', tracks=Track.query.all())
    else:
        trackName = Track.query.filter_by(id=trackId).first().name.replace(' ', '-').lower()
        webpage = f'tracks/{trackName}.html'
        return render_template(webpage)
