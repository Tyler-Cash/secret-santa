import sqlite3


def get_database(name):
    conn = sqlite3.connect(name)
    return conn