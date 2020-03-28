import os

from .file_analyser import FileAnalyser


class FolderAnalyser:

    def __init__(self, path: str):
        self.path = path
        self.get_files()
        self.python_files = self.get_files()
        self.joined_file = ''
        self.join_files()
        self.write_file()
        self.analysis = self.run_analysis()

    def get_files(self):
        python_files = []

        for dirname, dirnames, filenames in os.walk(self.path):

            for filename in filenames:
                if filename[-2:] == 'py':
                    python_files.append(os.path.join(dirname, filename))

        return python_files

    def join_files(self):
        for python_file in self.python_files:
            file = open(python_file, 'r')
            self.joined_file += file.read()
            file.close()

    def write_file(self):
        file = open('joined.py', 'w+')
        file.write(self.joined_file)
        file.close()

    def run_analysis(self):
        file_analyser = FileAnalyser('joined.py')
        return file_analyser

    def get_analysis(self):
        return self.analysis

    def __str__(self):
        return str(self.get_analysis())
