#!/bin/python
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os, json

app = Flask(__name__)

# General TODOs
# TODO: Create fake data for the second req we did for sprint 1
# TODO: Requirements 3 & 4

# TODO: Handle different user types correctly
@app.route("/")
def home(user=''):
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        if(user == 'Manager'):
          return render_template('users.html', user='Manager')
        elif(user == 'Employee'):
          return render_template('users.html', user='Employee')
        elif(user == 'Customer'):
          return render_template('users.html', user='Customer')
        # Redirect to the appropriate page here
        else:
          return 'Blah <a href="/logout">Logout</a>'


# TODO: Handle the correct user types
# TODO: Update users.json to use the correct user types. Placeholders work for now.
@app.route('/login', methods=['POST'])
def login():
    if not session.get('logged_in'):
        data = json.load(open('users.json'))
        for user in data["users"]:
            if user['username'] == request.form['username']:
                if user['password'] == request.form['password']:
                    if user['user-type'] == 'Manager':
                        session['logged_in'] = True
                        return home(user='Manager')
                    elif user["user-type"] == 'Employee':
                        session['logged_in'] = True
                        return home(user='Employee')
                    elif user['user-type'] == 'Customer':
                        session['logged_in'] = True
                        return home(user='Customer')
                    else:
                        render_template('login.html', error='Server error: invalid user type.')
                else:
                    # Wrong password
                    return render_template('login.html', error='Incorrect credentials.')
        else:
            return render_template('login.html', error='User not found in database.')
    else:
        return home()


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='127.0.0.1', port=5000)
