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
        except:
            print('Error opening database.')
            return False

    def query(self, sql: str):
        self.connect()
        try:
            self.db.execute(sql)
            print(f"Successfully exectued query: {sql}")
            self.db.commit()
            return True
        except:
            print(f"Error executing query: {sql}")
            return False

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
        except:
            print(f"Error executing query: {sql}")
            return False

        self.db.close()
