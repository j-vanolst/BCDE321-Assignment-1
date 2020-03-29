import re

from .class_definition import ClassAnalyser


class FileAnalyser:

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.lines = self.get_lines()
        self.get_classes_indexes()
        self.class_indexes = self.get_classes_indexes()
        self.class_names = self.get_class_names()
        self.class_definitions = self.get_class_definitions()
        self.class_analysers = self.create_class_analysers()
        self.class_count = len(self.class_indexes)

    def get_lines(self):
        try:
            file = open(self.file_path, 'r')

            lines = file.read()
            file.close()
            lines = lines.split('\n')

            return lines

        except:
            raise FileNotFoundError(f"Could not find file {self.file_path}")

    def get_classes_indexes(self):
        """
        Used to return the line numbers of classes in the file.
        """
        class_indexes = []

        for i in range(len(self.lines)):
            class_regex = re.search("^class ", self.lines[i])
            if class_regex:
                class_indexes.append(i)

        return class_indexes

    def get_class_names(self):
        """
        Extracts the class names from the line numbers.
        """
        class_names = []

        for class_index in self.class_indexes:
            line = self.lines[class_index]
            class_name = re.findall('[^class].*[a-zA-Z0-9][^:]', line)
            class_name = ''.join(class_name)

            # Remove space in front of class name
            class_name = class_name[1:]

            class_names.append(class_name)

        return class_names

    def get_class_definitions(self):
        """
        Extracts the class definition using the line numbers.
        This will be used to find the methods of the class.
        """
        class_definitions = []

        for i in range(len(self.class_indexes)):
            # Last Definition
            if i + 1 == len(self.class_indexes):
                class_definition = self.lines[self.class_indexes[i]:]
            else:
                class_definition = self.lines[self.class_indexes[i]:self.class_indexes[i+1]]
            class_definitions.append(class_definition)

        return class_definitions

    def create_class_analysers(self):
        class_analysers = []

        for i in range(len(self.class_indexes)):
            class_analyser = ClassAnalyser(
                self.class_names[i], self.class_definitions[i])

            class_analysers.append(class_analyser)

        return class_analysers

    def get_class_count(self):
        return self.class_count

    def __str__(self):
        output_string = f"{self.get_class_count()} Class(es) \n"

        for class_analyser in self.class_analysers:
            output_string += class_analyser.get_class_name() + '\n'
            output_string += str(class_analyser)

        return output_string


# a = FileAnalyser('database_config.py')
# # for class_analyser in a.class_analysers:
# #     print(class_analyser)
# print(a)
