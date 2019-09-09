from flask import render_template, flash, redirect, url_for

from flask_login import current_user, login_user

from webapp import app
from webapp.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        flash(f'Login requested for user {form.username.data}, rememberMe={form.rememberMe.data}')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
