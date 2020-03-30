from abc import ABCMeta, abstractmethod


class Database(metaclass=ABCMeta):

    def __init__(self, database: str, address: str = None,
                 username: str = None, password: str = None):
        self.address = address
        self.username = username
        self.password = password
        self.database = database
        self.db = None
        self.cursor = None

    def __str__(self):
        return(f"ServerAddress: '{self.address}' Username: '{self.username}'\
            Password: '{self.password}' Database: '{self.database}'")

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def query(self, sql: str):
        pass

    @abstractmethod
    def fetch(self):
        pass

