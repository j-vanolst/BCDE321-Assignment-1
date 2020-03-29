from abc import ABCMeta, abstractmethod


class Database(ABCMeta):

    def __init__(self, database: str, address: str = None, username: str = None, password: str = None):
        self.address = address
        self.username = username
        self.password = password
        self.database = database
        self.db = None
        self.cursor = None

    def __str__(self):
        return(f"ServerAddress: '{self.address}' Username: '{self.username}' Password: '{self.password}' Database: '{self.database}'")

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def query(self, sql: str):
        pass

    @abstractmethod
    def fetch(self):
        pass
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
