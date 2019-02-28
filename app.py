#!/bin/python
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os, json

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
        with open('users.json') as f:
            data = json.load(f)
            for user in data["users"]:
                if user['username'] == request.form['username']:
                    if user['password'] == request.form['password']:
                        if user['user-type'] == 'Manager':
                            session['logged_in'] = True
                            return home()
                        elif user["user-type"] == 'Employee':
                            session['logged_in'] = True
                            return home()
                        elif user['user-type'] == 'Customer':
                            session['logged_in'] = True
                            return home()
                        else:
                            render_template('login.html', error='Server error: invalid user type.')
                    else:
                        # Wrong password
                        return render_template('login.html', error='Incorrect credentials.')
    return render_template('login.html', error='User not found in database.')


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='127.0.0.1', port=5000)
