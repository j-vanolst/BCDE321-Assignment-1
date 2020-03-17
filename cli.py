from cmd import Cmd

from database_config import DatabaseConfig


class Menu(Cmd):

    def __init__(self):
        Cmd.__init__(self)
        self.prompt = ">>> "

    def do_dbconfig(self, file_path):
        if file_path:
            print(f"Reading config file {file_path}")
            database_config = DatabaseConfig(file_path)
            print(f"{database_config.get_user()} {database_config.get_password()}")
        else:
            print('file path not specified')

    def do_quit(self, line):
        print("Quitting...")
        return True


if __name__ == "__main__":
    menu = Menu()
    menu.cmdloop()
