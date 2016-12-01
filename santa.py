import user


def get_recipient(santaEmail, db):
    cur = db.cursor()
    ownID = user.get_id(santaEmail, db)
    cur.execute('SELECT Recipient FROM SANTA WHERE Santa=?', (ownID,))
    result = cur.fetchone()
    if result is not None:
        return user.get_email(result[0], db)
    else:
        return None


def add_recipient(santa_ID, recipient_ID, db):
    cur = db.cursor()
    cur.execute('INSERT INTO SANTA(Santa, Recipient) VALUES (?,?)', (santa_ID, recipient_ID))
    db.commit()
    return True
