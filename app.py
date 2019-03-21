#!/bin/python
import flask
from flask import Flask, render_template, request, session
import flask_login
from flask_login import current_user

import json
import os
from datetime import timedelta

app = Flask(__name__)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
app.secret_key = os.urandom(12)
accounts = json.load(open('users.json'))
# General TODOs
# TODO: Create fake data for the second req we did for sprint 1
# TODO: Requirements 3 & 4


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(user_id):
    if user_id not in accounts:
        return
    user = User()
    user.id = user_id
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in accounts:
        return
    user = User()
    user.id = email
    user.is_authenticated = request.form['password'] == accounts[email]['password']
    return user


# TODO: Handle different user types correctly
@app.route("/")
def home(user=''):


    if current_user.is_authenticated == False:
        # session['anonymous_user_id'] = user.id
        return render_template('login.html')
    elif current_user.is_authenticated == True:
        role=accounts[flask_login.current_user.id]["role"]
        # role = ''
        if role == 'Manager':
            return render_template('users.html', user='Manager', )
        elif role == 'Employee':
            return render_template('users.html', user='Employee')
        elif role == 'Customer':
            return render_template('users.html', user='Customer')
        # Redirect to the appropriate page here
        else:
            return 'Blah <a href="/logout">' + role + '</a>'
    else:
        return "You're retarded"





# TODO: Handle the correct user types
# TODO: Update users.json to use the correct user types. Placeholders work for now.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return render_template('login.html')
    email = flask.request.form['username']
    if email not in accounts:
        return render_template('login.html', error='Invalid credentials')
    if flask.request.form['password'] == accounts[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user, remember=False, duration=timedelta(seconds=5))
        return flask.redirect(flask.url_for('protected'))

    return render_template('login.html', error='Invalid credentials')


@app.route('/protected')
@flask_login.login_required
def protected():
    role=accounts[flask_login.current_user.id]["role"]
    if role == 'Manager':
        return render_template('users.html', user='Manager')
    elif role == 'Employee':
        return render_template('users.html', user='Employee')
    elif role == 'Customer':
        return render_template('users.html', user='Customer')
    else:
         return 'Blah <a href="/logout"> Youre name is: ' + role + '</a>'

@flask_login.login_required
@app.route('/account')
def account():
    role=accounts[flask_login.current_user.id]["role"]
    if role == 'Manager':
        return render_template('accounts.html', user='Manager')
    elif role == 'Employee':
        return render_template('accounts.html', user='Employee')
    elif role == 'Customer':
        return render_template('accounts.html', user='Customer')
    else:
         return 'Blah <a href="/logout"> Youre name is: ' + role + '</a>'

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return render_template('login.html', error='Logged out')


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='127.0.0.1', port=5000)
