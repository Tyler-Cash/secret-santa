import sqlite3


def get_database(name):
    conn = sqlite3.connect(name)
    return conn


def create_tables(db):
    conn = db

    conn.execute('''CREATE TABLE USER (
  UserID    INTEGER PRIMARY KEY,
  Name      TEXT NOT NULL,
  Password  TEXT NOT NULL);''')
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

    return conn
