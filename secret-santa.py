import flask
import os.path
from flask import Flask
import sqlite3
import database

app = Flask(__name__)
db = database.get_database("database.db")

@app.route('/')
def home():

    if 'identifier' in flask.session.keys():
        return flask.render_template('show-santa.html', user=flask.session['email'])
    else:
        return flask.render_template('login.html')


@app.route('/login', methods=['POST'])
def check_credentials():

    email = flask.request.form['email']
    password = flask.request.form['pass']

    if database.is_user(email, password, db):
        flask.session['identifier'] = database.create_session(email, db)
        flask.session['email'] = email
        return flask.redirect('/')
    return flask.render_template('login.html')


@app.route('/logout')
def logout():
    flask.session.pop('identifier', None)
    return flask.redirect('/')

if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    app.secret_key = 'super secret key'
    app.run()
