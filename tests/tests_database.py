import os
from unittest import TestCase
from database import create_tables, get_database
import sqlite3

DATABASE_NAME = "test.db"


class TestCreate_tables(TestCase):
    def create_db(self):
        if os.path.isfile(DATABASE_NAME):
            os.remove(DATABASE_NAME)
        db = get_database(DATABASE_NAME)
        if db is None:
            self.fail("No database created")

        return db

    def test_family_create(self):
        db = self.create_db()
        create_tables(db)

        cur = db.cursor()

        cur.execute("pragma table_info(FAMILY);")
        res = cur.fetchall()
        if len(res) is not 2:
            self.fail("Family table has incorrect amount of columns")

        if res[0][1] != "FamilyID":
            self.fail("First column should be called 'FamilyID'")

        if res[0][2] != "INTEGER":
            self.fail("First column should be of data type INTEGER")

        if res[1][1] != "Description":
            self.fail("Second column should be 'Description'")

        if res[1][2] != "TEXT":
            self.fail("Second column should be of data type TEXT")

    def test_interest_create(self):
        db = self.create_db()
        create_tables(db)

        cur = db.cursor()

        cur.execute("pragma table_info(INTEREST);")
        res = cur.fetchall()

        if len(res) is not 3:
            self.fail("Interest table has incorrect amount of columns")

        # First column
        if res[0][1] != "InterestID":
            self.fail("First column should be called 'InterestID'")

        if res[0][2] != "INTEGER":
            self.fail("First column should be of data type INTEGER")

        # Second column
        if res[1][1] != "Description":
            self.fail("Second column should be 'Description'")

        if res[1][2] != "TEXT":
            self.fail("Second column should be of data type TEXT")

        # Third column
        if res[2][1] != "UserID":
            self.fail("Third column should be 'Description'")

        if res[2][2] != "INTEGER":
            self.fail("Third column should be of data type INTEGER")

    def test_santa_create(self):
        db = self.create_db()
        create_tables(db)

        cur = db.cursor()

        cur.execute("pragma table_info(SANTA);")
        res = cur.fetchall()

        if len(res) is not 3:
            self.fail("Santa table has incorrect amount of columns")

        # First column
        if res[0][1] != "SantaID":
            self.fail("First column should be called 'SantaID'")

        if res[0][2] != "INTEGER":
            self.fail("First column should be of data type INTEGER")

        # Second column
        if res[1][1] != "Santa":
            self.fail("Second column should be 'Santa'")

        if res[1][2] != "INTEGER":
            self.fail("Second column should be of data type INTEGER")

        # Third column
        if res[2][1] != "Recipient":
            self.fail("Third column should be 'Recipient'")

        if res[2][2] != "INTEGER":
            self.fail("Third column should be of data type INTEGER")

    def test_session_create(self):
        db = self.create_db()
        create_tables(db)

        cur = db.cursor()

        cur.execute("pragma table_info(SESSION);")
        res = cur.fetchall()

        if len(res) is not 3:
            self.fail("Session table has incorrect amount of columns")

        # First column
        if res[0][1] != "SessionID":
            self.fail("First column should be called 'SessionID'")

        if res[0][2] != "INTEGER":
            self.fail("First column should be of data type INTEGER")

        # Second column
        if res[1][1] != "Secret":
            self.fail("Second column should be 'Secret'")

        if res[1][2] != "TEXT":
            self.fail("Second column should be of data type TEXT")

        # Third column
        if res[2][1] != "UserSession":
            self.fail("Third column should be 'Recipient'")

        if res[2][2] != "INTEGER":
            self.fail("Third column should be of data type INTEGER")

    def test_session_create(self):
        db = self.create_db()
        create_tables(db)

        cur = db.cursor()

        cur.execute("pragma table_info(USER);")
        res = cur.fetchall()

        if len(res) is not 7:
            self.fail("User table has incorrect amount of columns")

        # First column
        if res[0][1] != "UserID":
            self.fail("First column should be called 'UserID'")

        if res[0][2] != "INTEGER":
            self.fail("First column should be of data type INTEGER")

        # Second column
        if res[1][1] != "FirstName":
            self.fail("Second column should be 'FirstName'")

        if res[1][2] != "TEXT":
            self.fail("Second column should be of data type TEXT")

        # Third column
        if res[2][1] != "LastName":
            self.fail("Third column should be 'LastName'")

        if res[2][2] != "TEXT":
            self.fail("Third column should be of data type TEXT")

        # Fourth column
        if res[3][1] != "Email":
            self.fail("Fourth column should be 'Email'")

        if res[3][2] != "TEXT":
            self.fail("Fourth column should be of data type TEXT")

        # Fifth column
        if res[4][1] != "Password":
            self.fail("Fifth column should be 'Password'")

        if res[4][2] != "TEXT":
            self.fail("Fifth column should be of data type TEXT")

        # Sixth column
        if res[5][1] != "Salt":
            self.fail("Sixth column should be 'Secret'")

        if res[5][2] != "TEXT":
            self.fail("Sixth column should be of data type TEXT")

        # Seventh column
        if res[6][1] != "FamilyID":
            self.fail("Seventh column should be called 'SessionID'")

        if res[6][2] != "INTEGER":
            self.fail("Seventh column should be of data type INTEGER")
