from cmd import Cmd

from database_config import DatabaseConfig


class Menu(Cmd):

    def __init__(self):
        Cmd.__init__(self)
        self.prompt = ">>> "

    def do_dbconfig(self, file_path: str):
        """
        Syntax: dbconfig [file_path]
        Load the specified database config from file
        :param file_path: a string representing the path to the database config file
        :return: None
        """
        if file_path:
            print(f"Reading config file {file_path}")
            database_config = DatabaseConfig(file_path)
            print(database_config)
        else:
            print('file path not specified')

    def do_quit(self, line):
        print("Quitting...")
        return True


if __name__ == "__main__":
    menu = Menu()
    menu.cmdloop()
