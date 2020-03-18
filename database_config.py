import configparser


class DatabaseConfig:

    def __init__(self, config_file='db.conf'):
        self.config = configparser.ConfigParser()
        self.config_file = config_file
        self.__address = None
        self.__username = None
        self.__password = None
        self.__database = None
        self.read_config()

    def __str__(self):
        return f"ServerAddress: '{self.__address}' Username: '{self.__username}' Password: '{self.__password}' Database: '{self.__database}'"

    def read_config(self):
        self.config.read(self.config_file)

        # Check if the database section exists in the config file
        if 'Database' in self.config:
            config_section = self.config['Database']
        else:
            raise SectionNotPresent('Database section not present')

        # Check if the fields exist in the database section
        fields = ['ServerAddress', 'Username', 'Password', 'DatabaseName']
        for field in fields:
            if not field in config_section:
                raise FieldNotPresent(
                    f"Field {field} doesn't exist in database section of config file")

        # If all fields are present, set the attributes
        self.__address = config_section['ServerAddress']
        self.__username = config_section['Username']
        self.__password = config_section['Password']
        self.__database = config_section['DatabaseName']

    def get_address(self):
        return self.__address

    def get_user(self):
        return self.__username

    def get_password(self):
        return self.__password

    def get_name(self):
        return self.__database


class SectionNotPresent(Exception):

    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f"SectionNotPresent, {self.message}"
        else:
            return "SectionNotPresent has been raised"


class FieldNotPresent(Exception):

    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f"FieldNotPresent, {self.message}"
        else:
            return "FieldNotPresent has been raised"
