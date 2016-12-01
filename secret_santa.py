import json
import uuid

import flask
import time
from flask import request, redirect, render_template, Flask
from validate_email import validate_email

import database
import interest
import santa
import session
import user

app = Flask(__name__)
# FIXME
db = database.get_database("database.db")


@app.route('/')
def home():
    cookie_secret = request.cookies.get('user_secret')
    user_id = session.get_session(cookie_secret, db)
    if user_id is not None:
        email = user.get_email(user_id, db)
        first_name = user.get_name(email, db)
        if first_name is not None:
            recipient_email = santa.get_recipient(email, db)
            recipient_name = user.get_name(recipient_email, db)
            recipient_last_name = user.get_last_name(recipient_email, db)
            if recipient_name is not None and recipient_last_name is not None:
                recipient_name = recipient_name + " " + recipient_last_name
                return render_template('show-santa.html', firstName=None, recipient_name=recipient_name)
            return render_template('show-santa.html', firstName=first_name, recipient_name=None)
        else:
            return redirect(flask.url_for('logout'))
    else:
        return render_template('login.html')


@app.route('/ajax-get-recipients-interests')
def ajax_get_recipients_interests():
    cookie_secret = request.cookies.get('user_secret')
    user_id = session.get_session(cookie_secret, db)
    if user_id is not None:
        email = user.get_email(user_id, db)
        recipientEmail = santa.get_recipient(email, db)
        results = interest.get_interest(recipientEmail, db)

        return json.dumps({'success': True, 'outcome': results}), 200, {
            'ContentType': 'application/json'}


@app.route('/ajax-get-interests')
def ajax_get_interests():
    cookie_secret = request.cookies.get('user_secret')
    user_id = session.get_session(cookie_secret, db)
    if user_id is not None:
        email = user.get_email(user_id, db)
        results = interest.get_interest(email, db)
        totalInterests = len(results)

        return json.dumps({'success': True, 'outcome': results}), 200, {
            'ContentType': 'application/json'}


@app.route('/ajax-add-interest')
def ajax_add_interest():
    time.sleep(0.4)
    cookie_secret = request.cookies.get('user_secret')
    user_id = session.get_session(cookie_secret, db)
    if user_id is not None:
        email = user.get_email(user_id, db)
        description = request.args.get('description')

        if description is "":
            return json.dumps({'success': False,
                               'reason': 'Please don\'t submit an empty interest'}), 200, {
                       'ContentType': 'application/json'}

        if interest.add_interest(email, description, db):
            return json.dumps({'success': True}), 200, {
                'ContentType': 'application/json'}
        else:
            return json.dumps({'success': False,
                               'reason': 'Something went wrong adding interest, please email contact@tylercash.xyz if problem persists.'}), 200, {
                       'ContentType': 'application/json'}


@app.route('/ajax-delete-interest-<interestID>')
def ajax_delete_interest(interestID):
    cookie_secret = request.cookies.get('user_secret')
    user_id = session.get_session(cookie_secret, db)
    if user_id is not None:
        email = user.get_email(user_id, db)
        if interest.delete_interest(email, interestID, db):
            return json.dumps({'success': True}), 200, {
                'ContentType': 'application/json'}
        else:
            return json.dumps({'success': False}), 200, {
                'ContentType': 'application/json'}


@app.route('/ajaxlogin')
def ajax_check_credentials():
    email = request.args.get('email')
    password = request.args.get('pass')

    if user.is_user(email, password, db):
        login_cookie = generate_session(email)
        if login_cookie is not -1:
            return json.dumps({'success': True, 'outcome': '<p>Successfully logged in</p>', 'redirect': '/',
                               'user_secret': login_cookie}), 200, {
                       'ContentType': 'application/json'}
        else:
            return json.dumps(
                {'success': False,
                 'outcome': '<p>Something went wrong logging you in, please email contact@tylercash.xyz.</p>',
                 'redirect': '/'}), 200, {
                       'ContentType': 'application/json'}
    return json.dumps({'success': False, 'outcome': '<p>Username and password not found.</p>', 'redirect': '/'}), 200, {
        'ContentType': 'application/json'}


@app.route('/AJAXsignup')
def ajax_create_new_user():
    email = request.args.get('email')
    if user.get_name(email, db) is None:
        families = user.get_families(db)
        firstName = request.args.get('fName')
        lastName = request.args.get('lName')
        password = request.args.get('pass')
        uselessPassword = request.args.get('uselessPass')
        family = request.args.get('family')

        if not len(firstName) > 0 and len(lastName) > 0:
            return json.dumps({'success': False,
                               'outcome': '<p>Name appears to be invalid, please ensure to:</p><ul><li>Make sure to enter your first and last name</li></ul>'}), \
                   200, {
                       'ContentType': 'application/json'}
        if not validate_email(email):
            return json.dumps({'success': False,
                               'outcome': '<p>Email appears to be invalid, please ensure to:</p><ul><li>Enter a valid email address</li><li>The email account is active</li></ul>'}), \
                   200, {
                       'ContentType': 'application/json'}

        if not len(password) > 0:
            return json.dumps({'success': False,
                               'outcome': '<p>No password was entered, please ensure to:</p><ul><li>Enter a password</li></ul>'}), \
                   200, {
                       'ContentType': 'application/json'}
        if not uselessPassword == password:
            return json.dumps({'success': False,
                               'outcome': '<p>Provided passwords don\'t match, please ensure that:</p><ul><li>The passwords match</li></ul>'}), 200, {
                       'ContentType': 'application/json'}
        try:
            familyExists = False
            for familySingle in families:
                if int(family) is familySingle[0]:
                    familyExists = True
                    break
            if not familyExists:
                return json.dumps({'success': False,
                                   'outcome': '<p>Provided family was invalid, please ensure to:</p><ul><li>Select a family</li></ul>'}), 200, {
                           'ContentType': 'application/json'}
        except(TypeError):
            return json.dumps({'success': False,
                               'outcome': '<p>Provided family was invalid, please ensure to:</p><ul><li>Select a family</li></ul>'}), 200, {
                       'ContentType': 'application/json'}

        if not user.create_user(firstName, lastName, email, password, family, db):
            return json.dumps({'success': False,
                               'outcome': '<p>Account creation failed. Please email contact@tylercash.xyz if this issue persists</p>'}), 500, {
                       'ContentType': 'application/json'}

        login_cookie = generate_session(email)
        return json.dumps({'success': True, 'outcome': '<p>Successfully created account</p>', 'redirect': '/',
                           'user_secret': login_cookie}), 200, {
                   'ContentType': 'application/json'}
    else:
        return json.dumps({'success': False, 'outcome': '<p>Account creation failed. Email already registered.</p>',
                           'redirect': '/'}), 200, {
                   'ContentType': 'application/json'}


@app.route('/logout')
def logout():
    cookie_secret = request.cookies.get('user_secret')
    user_id = session.get_session(cookie_secret, db)
    session.stop_session(user_id, db)
    return redirect('/')


@app.route('/signup', methods=['GET', 'POST'])
def create_new_user():
    user_secret = request.cookies.get('user_secret')
    if verify_cookie(user_secret) is False:
        families = user.get_families(db)
        return render_template('signup.html', families=families)
    else:
        return redirect('/')


@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy-policy.html')


@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'GET':
        return render_template('reset-password.html')
    else:
        email = request.form['email']
        if email is None:
            return render_template('notification.html', message='Error, no email provided.')
        UserID = user.get_id(email, db)
        secret = str(uuid.uuid4().hex.upper()[0:25])
        db.execute('INSERT INTO RESET(Secret, PasswordToReset) VALUES (?,?)', (secret, UserID))
        db.commit()
        if user.email_user(
                                "<p>A password request has been made. Don't click on this link unless you requested a password reset</p><p><a href=https://santa.tylercash.xyz/reset-" + secret + ">Click here to reset your password</a></p>",
                                email, db):
            return render_template('notification.html', message='An email has been sent to the provided email address')
        else:
            return render_template('notification.html',
                                   message='Email failed, please send an email to contact@tylercash.xyz')

@app.route('/reset-<secret>', methods=['GET', 'POST'])
def accept_new_pass(secret):
    cur = db.cursor()
    if request.method == 'GET':
        cur.execute('SELECT * FROM RESET WHERE Secret=?', (secret,))
        res = cur.fetchall()

        if len(res) is 0:
            return render_template('notification.html', message='It appears this link isn\'t a valid password reset link')

        return render_template('new-password.html', secret=secret)
    else:
        if request.form['password'] != request.form['confirm-password']:
            return render_template('notification.html', message='Passwords were not the same. Please reopen the link, or push the back button.')
        cur.execute('SELECT PasswordToReset FROM RESET WHERE Secret=?', (secret,))
        res = cur.fetchall()

        if len(res) is 0:
            return render_template('notification.html',
                                   message='Something went wrong when resetting the password')

        userID = res[0][0]
        user.rewrite_password(request.form['password'], userID, db)
        return redirect('/')



def generate_session(email):
    user_secret = session.create_session(email, db)
    if user_secret is -1:
        return -1
    return user_secret


def verify_cookie(cookie_secret):
    if session.get_session(cookie_secret, db) is None:
        return False
    else:
        return True


if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    app.secret_key = 'super secret key'
    app.run(host='0.0.0.0')
