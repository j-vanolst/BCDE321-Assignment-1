from cmd import Cmd

# Local Imports
from database_config import DatabaseConfig
from database.mysqldb import MySQLDB
from analyser.file_analyser import FileAnalyser


class Menu(Cmd):

    def __init__(self):
        Cmd.__init__(self)
        self.prompt = ">>> "
        self.dbconfig = None
        self.db = None

    def do_dbconfig(self, file_path: str):
        """
        Syntax: dbconfig [file_path]
        Load the specified database config from file
        :param file_path: a string representing the path to the database config file
        :return: None
        """
        if file_path:
            print(f"Reading config file {file_path}")
            self.dbconfig = DatabaseConfig(file_path)
            print(self.dbconfig)
        else:
            print('file path not specified')

    def do_dbconnect(self, line):
        """
        Syntax: dbconnect
        Connect to the database after loading configuration from file
        :return: None
        """
        # Check if we have loaded a database configuration
        if self.dbconfig:
            self.db = MySQLDB(address=self.dbconfig.get_address(), username=self.dbconfig.get_username(),
                              password=self.dbconfig.get_password(), database=self.dbconfig.get_database())
            self.db.connect()
        else:
            print("You have not loaded a database config using dbconfig")

    def do_dbquery(self, sql: str):
        """
        Syntax: dbquery [sql]
        Execute the specified sql query
        :param sql: a string representing the sql query
        :return: None
        """
        # Check if we have connected to a database
        if self.db:
            self.db.query(sql)
        else:
            print("You have not connected to a database using dbconnect")

    def do_dbfetch(self, sql: str):
        """
        Syntax: dbquery [sql]
        Execute the specified sql query
        :param sql: a string representing the sql query
        :return: None
        """
        # Check if we have connected to a database
        if self.db:
            print(self.db.fetch(sql))
        else:
            print("You have not connected to a database using dbconnect")

    def do_analyse(self, file_path: str):
        """
        Syntax: analyse [file_path]
        Run an analysis on a file
        :param file_path: a string representing the path to the file for analysis
        :return: None
        """
        file_analyser = FileAnalyser(file_path)
        print(file_analyser)

    def do_quit(self, line):
        print("Quitting...")
        return True


if __name__ == "__main__":
    menu = Menu()
    menu.cmdloop()
