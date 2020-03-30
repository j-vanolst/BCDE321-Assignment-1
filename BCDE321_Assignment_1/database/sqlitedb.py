import sqlite3

from .database import Database


class Sqlite(Database):

    def __init__(self, database):
        super().__init__(database)

    def connect(self):
        try:
            self.db = sqlite3.connect(self.database)
            print('Successfully opened database.')
            return True
        except DatabaseConnectError:
            print('Error opening database.')
            raise DatabaseConnectError('Could not connect to database')

    def query(self, sql: str):
        self.connect()
        try:
            self.db.execute(sql)
            print(f"Successfully exectued query: {sql}")
            self.db.commit()
            return True
        except DatabaseQueryError:
            print(f"Error executing query: {sql}")
            raise DatabaseQueryError(f"Could not execute query {sql}")

        self.db.close()

    def fetch(self, sql: str):
        self.connect()

        results = []

        try:
            cursor = self.db.execute(sql)
            print(f"Successfully executed query: {sql}")

            for result in cursor:
                results.append(result)

            return results

        except DatabaseQueryError:
            print(f"Error executing query: {sql}")
            raise DatabaseQueryError(f"Could not execute query {sql}")

        self.db.close()


class DatabaseConnectError(Exception):

    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f"DatabaseConnectError, {self.message}"
        else:
            return "DatabaseConnectError has been raised"


class DatabaseQueryError(Exception):

    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f"DatabaseQueryError, {self.message}"
        else:
            return "DatabaseQueryError has been raised"
