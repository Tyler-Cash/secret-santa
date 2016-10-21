import os
import uuid


def create_session(email, db):
    cur = db.cursor()

    session = str(uuid.UUID(bytes=os.urandom(16)))
    cur.execute('SELECT USERID FROM USER WHERE Email=UPPER(?)', (email,))
    user_id = cur.fetchone()
    if user_id is not None:
        user_id = user_id[0]
    else:
        return -1
    cur.execute('DELETE FROM SESSION WHERE UserSession=?', (user_id,))
    cur.execute('INSERT INTO SESSION(secret, UserSession) VALUES (?, ?)', (session, user_id))
    db.commit()

    return session


def get_session(cookie_secret, db):
    cur = db.cursor()
    cur.execute('SELECT UserSession FROM SESSION WHERE Secret=?;', (cookie_secret,))
    result = cur.fetchone()
    if result is not None:
        result = result[0]
        return result
    else:
        return None

def stop_session(user_id, db):
    cur = db.cursor()
    cur.execute('DELETE FROM SESSION WHERE UserSession=?', (user_id,))
    db.commit()
    return True