from flask import session, request, redirect, render_template, Flask
from validate_email import validate_email

import database
import user

app = Flask(__name__)
db = database.get_database("database.db")


@app.route('/')
def home():
    if 'identifier' in session.keys():
        first_name = user.get_name(session['email'], db)
        return render_template('show-santa.html', firstName=first_name)
    else:
        return render_template('login.html')


@app.route('/login', methods=['POST'])
def check_credentials():
    email = request.form['email']
    password = request.form['pass']

    if user.is_user(email, password, db):
        session['identifier'] = user.create_session(email, db)
        session['email'] = email
        return redirect('/')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('identifier', None)
    return redirect('/')


@app.route('/signup', methods=['GET', 'POST'])
def create_new_user():
    if request.method == 'POST':
        form = request.form
        if not validate_email(form['email']):
            return 'email invalid'
        if not len(form['fName']) > 0 and len(form['lName']) > 0:
            return 'name appears to be invalid'
        if not len(form['pass']) > 0 and form['uselessPassword'] == form['pass']:
            return 'no password entered'

        if not user.create_user(form['fName'], form['lName'], form['email'], form['pass'], db):
            return 'account creation failed, please email contact@tylercash.xyz'

        return redirect('/')
    else:
        return render_template('signup.html')



if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    app.secret_key = 'super secret key'
    app.run()
