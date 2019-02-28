#!/bin/python
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os

app = Flask(__name__)

@app.route("/")
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        # Redirect to the appropriate page here
        return 'Blah <a href="/logout">Logout</a>'


@app.route('/login', methods=['POST'])
def login():
    if not session.get('logged_in'):
        error = None
        if request.form['password'] == 'password' and request.form['username'] == 'admin':
            session['logged_in'] = True
            return home()
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='127.0.0.1', port=5000)
