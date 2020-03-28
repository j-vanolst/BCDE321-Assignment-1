import subprocess


class Graph:

    def __init__(self, path: str):
        self.path = path
        try:
            self.run_pyreverse()
        except:
            print(
                "Error running pyreverse. Please check you have specified a python file/package correctly.")

    def run_pyreverse(self):
        subprocess.run(['pyreverse', '-ASmy', '-o', 'png', self.path])

    def notify(self):
        return f"Generated class and package diagram for {self.path}.\nLook in current directory for classes.png and packages.png"
