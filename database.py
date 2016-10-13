import sqlite3

import bcrypt as bcrypt


def get_database(name):
    conn = sqlite3.connect(name, check_same_thread=False)
    return conn


def create_tables(db):
    conn = db

    conn.execute('''CREATE TABLE USER (
  UserID    INTEGER PRIMARY KEY,
  Name      TEXT NOT NULL,
  Password  TEXT NOT NULL,
  Salt      TEXT NOT NULL);''')
    conn.commit()

    conn.execute('''CREATE TABLE INTEREST (
  InterestID  INTEGER PRIMARY KEY,
  Description TEXT NOT NULL,
  UserID      INTEGER,

  FOREIGN KEY (UserID) REFERENCES USER (UserID));''')
    conn.commit()

    conn.execute('''CREATE TABLE FAMILY (
  FamilyID    INTEGER PRIMARY KEY,
  Description TEXT NOT NULL,
  UserID      INTEGER,

  FOREIGN KEY (UserID) REFERENCES USER (UserID));''')
    conn.commit()

    conn.execute('''CREATE TABLE SANTA (
  SantaID     INTEGER PRIMARY KEY,
  Santa       INTEGER,
  Recipient   INTEGER,

  FOREIGN KEY (Santa) REFERENCES USER (UserID),
  FOREIGN KEY (Recipient) REFERENCES USER (UserID));''')
    conn.commit()

    # FIXME add timeout for session
    conn.execute('''CREATE TABLE SESSION (
      SessionID     INTEGER PRIMARY KEY,
      Secret       INTEGER);''')
    conn.commit()

    return conn


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

    cur.execute('INSERT INTO SESSION(secret) VALUES (?)', (session,))
    cur.commit()

    return session

    return