from cmd import Cmd

# Local Imports
from database_config import DatabaseConfig
from database.mysqldb import MySQLDB
from database.sqlitedb import Sqlite
from analyser.file_analyser import FileAnalyser
from analyser.folder_analyser import FolderAnalyser
from graph import Graph


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
        :param file_path: a string representing the path to the database
        config file
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
            # Determine what type of database we are using
            if self.dbconfig.get_type() == 'mysql':
                self.db = MySQLDB(address=self.dbconfig.get_address(),
                                  username=self.dbconfig.get_username(),
                                  password=self.dbconfig.get_password(),
                                  database=self.dbconfig.get_database())
                self.db.connect()
            elif self.dbconfig.get_type() == 'sqlite':
                self.db = Sqlite(self.dbconfig.get_database())
                self.db.connect()
        else:
            print("You have not loaded a database config using dbconfig")

    def do_dbcreatetable(self, line):
        """
        Syntax: dbcreatetable
        Creates a table for storing analyses if the table doesn't
        already exist
        :return: None
        """
        sql = 'create table if not exists analysis\
            (id int primary key auto_increment, analysis varchar(100000),\
                path varchar(100))'
        if self.dbconfig.get_type() == 'sqlite':
            sql = 'create table if not exists analysis\
                (id integer primary key autoincrement,\
                    analysis varchar(100000), path varchar(100))'
        if self.db:
            self.db.query(sql)
        else:
            print("You have not connected to a database using dbconnect")

    def do_dblistanalyses(self, line):
        """
        Syntax dblistanalyses
        Lists currently stored analyses in the database
        :return: None
        """
        sql = 'select path from analysis'
        if self.db:
            self.do_dbfetch(sql)
        else:
            print("You have not connected to a database using dbconnect")

    def do_dbselectanalysis(self, analysis):
        """
        Syntax dbselectanalysis [analysis]
        Return an analysis from the database, you can get a list of stored
        analyses with the dblistanalyses command
        :param analysis: a string representing the record you want to access
        :return: None
        """
        sql = f"select * from analysis where path ='{analysis}'"
        if self.db:
            self.do_dbfetch(sql)
        else:
            print("You have not connected to a database using dbconnect")

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

    def do_analyse(self, path: str):
        """
        Syntax: analyse [file_path]
        Run an analysis on a file
        :param file_path: a string representing the path to the file for
        analysis
        :return: None
        """
        file_analyser = FileAnalyser(path)
        print(file_analyser)

        if self.db:
            sql = f"insert into analysis (analysis, path) values\
                ('{str(file_analyser)}', '{path}')"
            self.do_dbquery(sql)
        else:
            print("If you want the analysis stored in the database,\
                please connect to a database using dbconnect first.")

    def do_analyse_folder(self, path: str):
        """
        Syntax: analyse [folder_path]
        Run an analysis on a folder
        :param folder_path: a string representing the path to the folder
        for analysis
        :return: None
        """
        folder_analyser = FolderAnalyser(path)
        print(folder_analyser)

        if self.db:
            sql = f"insert into analysis (analysis, path) values\
                ('{str(folder_analyser)}', '{path}')"
            self.do_dbquery(sql)
        else:
            print("If you want the analysis stored in the database,\
                please connect to a database using dbconnect first.")

    def do_graph(self, path: str):
        """
        Syntax: graph [file/package path]
        Generate a class and package diagram from a file/package
        :param path: a string representing the path to the file/package
        :return: None
        """
        graph = Graph(path)
        print(graph.notify())

    def do_quit(self, line):
        print("Quitting...")
        return True


if __name__ == "__main__":
    menu = Menu()
    menu.cmdloop()
