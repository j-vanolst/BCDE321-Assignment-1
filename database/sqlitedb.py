import sqlite3

from .database import Database


class Sqlite(Database):

    def __init__(self, database):
        super().__init__(database)

    def connect(self):
        try:
            self.db = sqlite3.connect(self.database)
            print('Successfully opened database.')
        except:
            print('Error opening database.')

    def query(self, sql: str):
        self.connect()
        self.db.execute(sql)
        try:
            self.db.execute(sql)
            print(f"Successfully exectued query: {sql}")
            self.db.commit()
        except:
            print(f"Error executing query: {sql}")

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


# test = Sqlite(database='test.db')
# test.connect()
# test.query('create table test (name text, age int)')
# test.query("insert into test values ('jos', 22)")
# print(test.fetch("select * from test"))
