import database
import user
from flask import session, request, redirect, render_template, Flask

app = Flask(__name__)
db = database.get_database("database.db")


@app.route('/')
def home():
    if 'identifier' in session.keys():
        return render_template('show-santa.html', user=session['email'])
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


if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    app.secret_key = 'super secret key'
    app.run()
