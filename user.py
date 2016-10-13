import bcrypt


def generate_salt():
    return bcrypt.gensalt()


def hash_password(password, salt):
    result = bcrypt.hashpw(password, salt).decode('utf-8')
    return result


def is_user(email, password, db):
    cur = db.cursor()

    cur.execute('SELECT Salt FROM USER WHERE Name=?;', (email,))
    salt = cur.fetchall()

    if len(salt) is 0:
        return False

    salt = salt[0][0]

    password = hash_password(password.encode('utf-8'), salt.encode('utf-8'))
    cur.execute('SELECT * FROM USER WHERE Name LIKE UPPER(?) AND Password=?;', (email, password))

    result = cur.fetchall()
    if len(result) is not 0:
        return True
    else:
        return False


def create_session(email, db):
    cur = db.cursor()

    session = generate_salt()
    cur.execute('SELECT USERID FROM USER WHERE Name=?', (email,))
    userID = cur.fetchone()
    userID = userID[0]

    cur.execute('INSERT INTO SESSION(secret, UserSession) VALUES (?, ?)', (session, userID))
    db.commit()

    return session