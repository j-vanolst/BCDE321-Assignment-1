import configparser


class DatabaseConfig:

    def __init__(self, config_file='db.conf'):
        self.config = configparser.ConfigParser()
        self.config_file = config_file
        self.__db_address = None
        self.__db_user = None
        self.__db_password = None
        self.__db_name = None
        self.read_config()

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
        self.__db_address = config_section['ServerAddress']
        self.__db_user = config_section['Username']
        self.__db_password = config_section['Password']
        self.__db_name = config_section['DatabaseName']

    def get_address(self):
        return self.__db_address

    def get_user(self):
        return self.__db_user

    def get_password(self):
        return self.__db_password

    def get_name(self):
        return self.__db_name


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
