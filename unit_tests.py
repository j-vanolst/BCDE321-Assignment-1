import unittest
import os
from filehash import FileHash

# Local Imports
from BCDE321_Assignment_1.database_config import DatabaseConfig
from BCDE321_Assignment_1.database.mysqldb import MySQLDB
from BCDE321_Assignment_1.database.sqlitedb import Sqlite
from BCDE321_Assignment_1.analyser.file_analyser import FileAnalyser
from BCDE321_Assignment_1.analyser.folder_analyser import FolderAnalyser
from BCDE321_Assignment_1.graph import Graph


class DatabaseConfigTests(unittest.TestCase):
    def setUp(self):
        self.database_config = DatabaseConfig('test_files/test.conf')

    def tearDown(self):
        pass

    def test_01(self):
        """
        Check the imported database config values are correct
        Based on test config in test_files/test.conf file
        """
        self.assertTrue(self.database_config.get_address() == '127.0.0.1')
        self.assertTrue(self.database_config.get_username() == 'root')
        self.assertTrue(self.database_config.get_password() == 'test')
        self.assertTrue(self.database_config.get_database() == 'python_uml')
        self.assertTrue(self.database_config.get_type() == 'mysql')

    def test_02(self):
        """
        Deliberately check incorrect values - should correctly assertFalse
        Based on test config in test_files/test.conf file
        """
        self.assertFalse(self.database_config.get_address() == '123.456.789.0')
        self.assertFalse(self.database_config.get_username() == 'admin')
        self.assertFalse(self.database_config.get_password() == 'password')
        self.assertFalse(self.database_config.get_database() == 'my_database')
        self.assertFalse(self.database_config.get_type() == 'sqlite')


class MySQLDatabaseTests(unittest.TestCase):
    """
    For this test suite to run correctly you (obviously) need to have a MySQL
    server running and correctly configured in the setUp() function below
    I have created a test table inside the python_uml database with the values for testing
    """

    def setUp(self):
        self.db = MySQLDB('127.0.0.1', 'root', 'test', 'python_uml')

    def tearDown(self):
        pass

    def test_01(self):
        """
        Check the database has been set correctly
        """
        self.assertTrue(self.db.address == '127.0.0.1')
        self.assertTrue(self.db.username == 'root')
        self.assertTrue(self.db.password == 'test')
        self.assertTrue(self.db.database == 'python_uml')

    def test_02(self):
        """
        Check whether we can connect to the database
        """
        self.assertTrue(self.db.connect() == True)

    def test_03(self):
        """
        Check fetching data from the database is correct
        """
        sql = "select name from test"
        self.assertTrue(self.db.fetch(sql)[0][0] == 'Jos')

    def test_04(self):
        """
        Check fetching data from the database, delibarately incorrect so assertFalse is used
        """
        sql = "select name from test"
        self.assertFalse(self.db.fetch(sql)[0][0] == 'Mark')


class SqliteDatabaseTests(unittest.TestCase):
    """
    This test suite uses the sqlite database stored in test_files/test.db
    """

    def setUp(self):
        self.db = Sqlite('test_files/test.db')

    def tearDown(self):
        pass

    def test_01(self):
        """
        Check the database has been set correctly
        """
        self.assertTrue(self.db.database == 'test_files/test.db')

    def test_02(self):
        """
        Check whether we can connect to the database
        """
        self.assertTrue(self.db.connect() == True)

    def test_03(self):
        """
        Check fetching data from the database is correct
        """
        sql = 'select name from test'
        self.assertTrue(self.db.fetch(sql)[0][0] == 'Jos')

    def test_04(self):
        """
        Check fetching data from the database, deliberately inncorrect so assertFalse is used
        """
        sql = 'select name from test'
        self.assertFalse(self.db.fetch(sql)[0][0] == 'Mark')


class FileAnalyserTests(unittest.TestCase):
    """
    File analysis will be run on test_files/test.py
    """

    def setUp(self):
        self.analyser = FileAnalyser('test_files/test.py')

    def tearDown(self):
        pass

    def test_01(self):
        """
        Check the number of classes has correctly been detected
        """
        self.assertTrue(self.analyser.get_class_count() == 2)

    def test_02(self):
        """
        Check the correct number of methods for each of the classes has been detected
        """
        self.assertTrue(
            self.analyser.class_analysers[0].get_method_count() == 2)
        self.assertTrue(
            self.analyser.class_analysers[1].get_method_count() == 3)

    def test_03(self):
        """
        Check the correct number of parameters for each method has been detected
        """
        self.assertTrue(
            len(self.analyser.class_analysers[0].method_parameters['__init__()']) == 2)
        self.assertTrue(
            len(self.analyser.class_analysers[0].method_parameters['greet()']) == 1)
        self.assertTrue(
            len(self.analyser.class_analysers[1].method_parameters['__init__()']) == 3)
        self.assertTrue(
            len(self.analyser.class_analysers[1].method_parameters['get_brand()']) == 1)
        self.assertTrue(
            len(self.analyser.class_analysers[1].method_parameters['get_colour()']) == 1)

    def test_04(self):
        """
        Check the number of detected classes is incorrect
        """
        self.assertFalse(self.analyser.get_class_count() == 1)

    def test_05(self):
        """
        Check the number of detected methods for each detected class is incorrect
        """
        self.assertFalse(
            self.analyser.class_analysers[0].get_method_count() == 1)
        self.assertFalse(
            self.analyser.class_analysers[1].get_method_count() == 9)

    def test_06(self):
        """
        Check the number of parameters for each detected method is incorrect
        """
        print(self.analyser.class_analysers[0].method_parameters)
        self.assertFalse(
            len(self.analyser.class_analysers[0].method_parameters['__init__()']) == 6)
        self.assertFalse(
            len(self.analyser.class_analysers[0].method_parameters['greet()']) == 4)
        self.assertFalse(
            len(self.analyser.class_analysers[1].method_parameters['__init__()']) == 6)
        self.assertFalse(
            len(self.analyser.class_analysers[1].method_parameters['get_brand()']) == 2)
        self.assertFalse(
            len(self.analyser.class_analysers[1].method_parameters['get_colour()']) == 4)


class FolderAnalyserTests(unittest.TestCase):
    """
    Folder analysis will be run on test_files folder
    which contains test.py and test2.py
    """

    def setUp(self):
        self.analyser = FolderAnalyser('test_files')

    def tearDown(self):
        pass

    def test_01(self):
        """
        Check the number of classes has been detected correctly
        """
        self.assertTrue(self.analyser.analysis.get_class_count() == 3)

    def test_02(self):
        """
        Check the number of methods for each detected class has been detected correctly
        """
        self.assertTrue(
            self.analyser.analysis.class_analysers[0].get_method_count() == 2)
        self.assertTrue(
            self.analyser.analysis.class_analysers[1].get_method_count() == 3)
        self.assertTrue(
            self.analyser.analysis.class_analysers[2].get_method_count() == 2)

    def test_03(self):
        """
        Check the number of attributes for each method of each class has been detected correctly
        """
        self.assertTrue(len(
            self.analyser.analysis.class_analysers[0].method_parameters['__init__()']) == 2)
        self.assertTrue(
            len(self.analyser.analysis.class_analysers[0].method_parameters['greet()']) == 1)

        self.assertTrue(len(
            self.analyser.analysis.class_analysers[1].method_parameters['__init__()']) == 3)
        self.assertTrue(len(
            self.analyser.analysis.class_analysers[1].method_parameters['get_brand()']) == 1)
        self.assertTrue(len(
            self.analyser.analysis.class_analysers[1].method_parameters['get_colour()']) == 1)

        self.assertTrue(len(
            self.analyser.analysis.class_analysers[2].method_parameters['__init__()']) == 2)
        self.assertTrue(len(
            self.analyser.analysis.class_analysers[2].method_parameters['get_type()']) == 1)

    def test_04(self):
        """
        Check the number of classes has been detected incorrectly
        """
        self.assertFalse(self.analyser.analysis.get_class_count() == 4)

    def test_05(self):
        """
        Check the number of methods for each detected class has been detected incorrectly
        """
        self.assertFalse(
            self.analyser.analysis.class_analysers[0].get_method_count() == 1)
        self.assertFalse(
            self.analyser.analysis.class_analysers[1].get_method_count() == 2)
        self.assertFalse(
            self.analyser.analysis.class_analysers[2].get_method_count() == 3)

    def test_06(self):
        """
        Check the number of attributes for each method of each class has been detected incorrectly
        """
        self.assertFalse(len(
            self.analyser.analysis.class_analysers[0].method_parameters['__init__()']) == 1)
        self.assertFalse(
            len(self.analyser.analysis.class_analysers[0].method_parameters['greet()']) == 2)

        self.assertFalse(len(
            self.analyser.analysis.class_analysers[1].method_parameters['__init__()']) == 1)
        self.assertFalse(len(
            self.analyser.analysis.class_analysers[1].method_parameters['get_brand()']) == 2)
        self.assertFalse(len(
            self.analyser.analysis.class_analysers[1].method_parameters['get_colour()']) == 3)

        self.assertFalse(len(
            self.analyser.analysis.class_analysers[2].method_parameters['__init__()']) == 1)
        self.assertFalse(len(
            self.analyser.analysis.class_analysers[2].method_parameters['get_type()']) == 2)


class GraphTests(unittest.TestCase):
    """
    To do this test I have supplied an already generated class diagram of test.py
    located in test_files/supplied_class_diagram.png
    This test will compare the file hashes of the generated png file with this using the filehash library
    """

    def setUp(self):
        self.graph = Graph('test_files/test.py')
        self.hasher = FileHash('md5')
        self.check_hash = self.hasher.hash_file(
            'test_files/supplied_class_diagram.png')

    def tearDown(self):
        pass

    def test_01(self):
        """
        Generate a new class diagram from test_files/test.py and 
        check the new md5 hash against the existing one
        """
        self.test_hash = self.hasher.hash_file('classes.png')
        self.assertTrue(self.test_hash == self.check_hash)
        os.remove('classes.png')


if __name__ == '__main__':
    unittest.main(verbosity=2)
