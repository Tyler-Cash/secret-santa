import os
import uuid


def create_session(email, db):
    cur = db.cursor()

    session = uuid.UUID(bytes=os.urandom(16))
    cur.execute('SELECT USERID FROM USER WHERE Email=UPPER(?)', (email,))
    user_id = cur.fetchone()
    if user_id is not None:
        user_id = user_id[0]
    else:
        return -1

    cur.execute('INSERT INTO SESSION(secret, UserSession) VALUES (?, ?)', (session.bytes, user_id))
    db.commit()

    return session.bytes