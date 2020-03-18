import mysql.connector

from .database import Database


class MySQLDB(Database):

    def __init__(self, address: str, username: str, password: str, database: str):
        super().__init__(address=address, username=username,
                         password=password, database=database)

    def connect(self):
        self.db = mysql.connector.connect(
            host=self.address, user=self.username, passwd=self.password, database=self.database)
        try:
            self.db = mysql.connector.connect(
                host=self.address, user=self.username, passwd=self.password, database=self.database)
            print("Successfully connected to the database.")
        except:
            print("Error connecting to the database.")

    def query(self, sql: str):
        """
        Used for all queries where data isn't being returned
        """
        self.connect()
        self.cursor = self.db.cursor()
        try:
            self.cursor.execute(sql)
            print(f"Successfully executed query: {sql}")
            self.db.commit()
            self.cursor.close()
            self.db.close()
        except:
            print(f"Error executing query: {sql}")

    def fetch(self, sql: str):
        """
        Used for queries where data is being returned i.e SELECT queries
        """
        self.connect()
        self.cursor = self.db.cursor()
        try:
            self.cursor.execute(sql)
            print(f"Successfully executed query: {sql}")
            results = self.cursor.fetchall()
            self.cursor.close()
            self.db.close()
            return results
        except:
            print(f"Error executing query: {sql}")
            return False


# test = MySQLDB('127.0.0.1', 'root', 'test', 'python_uml')
# print(test)
# test.connect()
# test.query("insert into test values ('jos')")
# print(test.fetch('select * from test'))
