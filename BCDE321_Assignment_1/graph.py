import subprocess


class Graph:

    def __init__(self, path: str):
        self.path = path
        try:
            self.run_pyreverse()
        except PyReverseError:
            print(
                "Error running pyreverse. Please check you have specified\
                    a python file/package correctly.")
            raise PyReverseError(
                "Error running pyreverse\
                    please check it is installed correctly")

    def run_pyreverse(self):
        subprocess.run(['pyreverse', '-ASmy', '-o', 'png', self.path])

    def notify(self):
        return f"Generated class and package diagram for {self.path}.\n\
            Look in current directory for classes.png and packages.png"


class PyReverseError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f"PyReverseError, {self.message}"
        else:
            return "PyReverseError has been raised"
