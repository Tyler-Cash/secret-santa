import smtplib
from sender_pass import sender_password
import bcrypt


def generate_salt():
    return bcrypt.gensalt().decode('utf-8')


def hash_password(password, salt):
    result = bcrypt.hashpw(password, salt).decode('utf-8')
    return result

def rewrite_password(password, userID, db):
    cur = db.cursor()
    email = get_email(userID, db)
    # TODO Extract into method
    cur.execute('SELECT Salt FROM USER WHERE Email=UPPER(?);', (email,))
    salt = cur.fetchall()

    if len(salt) is 0:
        return False

    salt = salt[0][0]

    hashed_password = hash_password(password.encode('utf-8'), salt.encode('utf-8'))
    if userID is None:
        return False
    cur.execute('UPDATE USER SET Password=? WHERE UserID=?', (hashed_password, userID))
    cur.execute('DELETE FROM RESET WHERE PasswordToReset=?', (userID,))
    db.commit()
    return True

def is_user(email, password, db):
    cur = db.cursor()

    cur.execute('SELECT Salt FROM USER WHERE Email=UPPER(?);', (email,))
    salt = cur.fetchall()

    if len(salt) is 0:
        return False

    salt = salt[0][0]

    password = hash_password(password.encode('utf-8'), salt.encode('utf-8'))
    cur.execute('SELECT * FROM USER WHERE USER.Email LIKE UPPER(?) AND Password=?;', (email, password))

    result = cur.fetchall()
    if len(result) is not 0:
        return True
    else:
        return False


def get_email(user_id, db):
    cur = db.cursor()
    cur.execute('SELECT Email FROM USER WHERE UserID=UPPER(?)', (user_id,))
    result = cur.fetchone()
    if result is None:
        return None
    else:
        return result[0]


def get_name(email, db):
    cur = db.cursor()
    cur.execute('SELECT FirstName FROM USER WHERE Email=UPPER(?)', (email,))
    result = cur.fetchone()
    if result is None:
        return None
    else:
        return result[0]


def get_id(email, db):
    cur = db.cursor()
    cur.execute('SELECT UserID FROM USER WHERE Email=UPPER(?)', (email,))
    result = cur.fetchone()
    if result is None:
        return None
    else:
        return result[0]


def create_user(first_name, last_name, email, password, familyID, db):
    salt = generate_salt()
    password = hash_password(password.encode('utf-8'), salt.encode('utf-8'))

    cur = db.cursor()

    cur.execute(
        'INSERT INTO USER (firstName, lastName, email, Password, Salt, FamilyID) VALUES (UPPER(?),UPPER(?),UPPER(?),?,?,?);',
        (first_name, last_name, email, password, salt, familyID))
    db.commit()

    return True


def get_families(db):
    cur = db.cursor()
    cur.execute('SELECT * FROM FAMILY')

    return cur.fetchall()


def get_from_family(db, family_ID):
    cur = db.cursor()
    cur.execute(
        'SELECT Email, UserID, USER.FamilyID,FAMILY.Description FROM USER INNER JOIN FAMILY ON FAMILY.FamilyID = USER.FamilyID  WHERE USER.FamilyID=?',
        (family_ID,))

    return cur.fetchall()


# Requires user pass to be stored in sender_password variable inside of sender_pass.py
def email_user(param, email, db):
    name = get_name(email, db)
    if name is None:
        return False

    sender = 'contact@tylercash.xyz'
    receivers = [email]
    message = """From: Secret Santa <contact@tylercash.xyz>
To: """ + name +""" <""" + email + """>
MIME-Version: 1.0
Content-type: text/html
Subject: Secret santa password reset
""" + param

    try:

        smtp_connection = smtplib.SMTP_SSL('mail.privateemail.com:465')
        smtp_connection.login(sender, sender_password)
        smtp_connection.sendmail(sender, receivers, message)
        smtp_connection.quit()
        return True
    except smtplib.SMTPException:
        print('Failed email to ' + email)


def get_last_name(email, db):
    cur = db.cursor()
    cur.execute('SELECT LastName FROM USER WHERE Email=UPPER(?)', (email,))
    result = cur.fetchone()
    if result is None:
        return None
    else:
        return result[0]