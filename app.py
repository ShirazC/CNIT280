#!/bin/python
"""
This is the main body of group 25's webapp.
"""
import json
import os
from datetime import timedelta

import flask
import flask_login
from flask import Flask, render_template
from flask_login import current_user

APP = Flask(__name__)
LOGIN_MANAGER = flask_login.LoginManager()
LOGIN_MANAGER.init_app(APP)
APP.secret_key = os.urandom(12)
ACCOUNTS = json.load(open('users.json'))
INVOICES = json.load(open('invoice.json'))
# General TODOs
# TODO: Create fake data for the second req we did for sprint 1
# TODO: Requirements 3 & 4


class User(flask_login.UserMixin):
    """
    TODO: Write docstring
    """
    pass


@LOGIN_MANAGER.user_loader
def user_loader(user_id):
    """
    TODO: Write docstring
    """
    if user_id not in ACCOUNTS:
        return
    user = User()
    user.id = user_id
    return user


@LOGIN_MANAGER.request_loader
def request_loader(request):
    """
    TODO: Write docstring
    """
    email = request.form.get('email')
    if email not in ACCOUNTS:
        return
    user = User()
    user.id = email
    user.is_authenticated = request.form['password'] == ACCOUNTS[email]['password']
    return user


# TODO: Handle different user types correctly
@APP.route("/")
def home():
    """
    TODO: Write docstring
    """
    if current_user.is_authenticated is False:
        # session['anonymous_user_id'] = user.id
        return render_template('login.html')
    role = ACCOUNTS[flask_login.current_user.id]["role"]

    if not role:
        return '<a href="/logout">Server Error</a>'

    return render_template('users.html', user=str(role))


# TODO: Handle the correct user types
# TODO: Update users.json to use the correct user types instead of placeholders.
@APP.route('/login', methods=['GET', 'POST'])
def login():
    """
    TODO: Write docstring
    """
    if flask.request.method == 'GET':
        return render_template('login.html')

    email = flask.request.form['username']

    if email not in ACCOUNTS:
        return render_template('login.html', error='Invalid credentials')

    if flask.request.form['password'] == ACCOUNTS[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user, remember=False, duration=timedelta(seconds=5))
        return flask.redirect(flask.url_for('protected'))

    return render_template('login.html', error='Invalid credentials')


@APP.route('/protected')
@flask_login.login_required
def protected():
    """
    TODO: Write docstring
    """
    if current_user.is_authenticated is False:
        return flask.redirect(flask.url_for('login'))

    role = ACCOUNTS[flask_login.current_user.id]["role"]

    if not role:
        return '<a href="/logout">Server Error</a>'

    return render_template('users.html', user=str(role))


@flask_login.login_required
@APP.route('/account')
def account():
    """
    TODO: Write docstring
    """
    if current_user.is_authenticated is False:
        return flask.redirect(flask.url_for('login'))

    role = ACCOUNTS[flask_login.current_user.id]["role"]

    if not role:
        return '<a href="/logout">Server Error</a>'

    return render_template('users.html', user=str(role))


@flask_login.login_required
@APP.route('/invoice')
def invoice():
    """
    TODO: Write docstring
    """
    if current_user.is_authenticated is False:
        return flask.redirect(flask.url_for('login'))

    role = ACCOUNTS[flask_login.current_user.id]["role"]

    if not role:
        return 'Blah <a href="/logout"> Youre name is: ' + role + '</a>'

    return render_template('users.html', user=str(role), labels=INVOICES)


@APP.route('/logout')
def logout():
    """
    TODO: Write docstring
    """
    flask_login.logout_user()
    return render_template('login.html', error='Logged out')


@LOGIN_MANAGER.unauthorized_handler
def unauthorized_handler():
    """
    TODO: Write docstring
    """
    return flask.redirect(flask.url_for('login'))


if __name__ == '__main__':
    APP.secret_key = os.urandom(12)
    APP.run(debug=True, host='127.0.0.1', port=5000)
