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
