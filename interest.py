import user


def get_interest(email, db):
    cur = db.cursor()

    cur.execute('SELECT UserID FROM USER WHERE Email=upper(?)', (email,))

    userID = cur.fetchone()[0]

    cur.execute('SELECT DESCRIPTION, InterestID FROM INTEREST WHERE UserID=?', (userID,))

    results = cur.fetchall()
    list = []
    for result in results:
        list.append('\'interest' + str(result[1]) + '\': \'' + result[0] + '\'')

    return results


def check_owner(interestID, db):
    cur = db.cursor()
    cur.execute('SELECT UserID FROM INTEREST WHERE InterestID=?', (interestID,))
    result = cur.fetchone()[0]
    cur.execute('SELECT Email FROM USER WHERE UserID=?', (result,))
    result = cur.fetchone()[0]
    return result


def delete_interest(email, interestID, db):
    if email.upper() == check_owner(interestID, db):
        cur = db.cursor()
        cur.execute('DELETE FROM INTEREST WHERE InterestID=?', (interestID,))
        db.commit()
        return True

    return False


def add_interest(email, description, db):
    cur = db.cursor()
    userID = user.get_id(email, db)

    cur.execute('INSERT INTO INTEREST(Description, UserID) VALUES (?, ?)', (description, userID))
    db.commit()

    return True