import re
from typing import List


class ClassAnalyser:

    def __init__(self, class_name: str, class_definition: List[str]):
        self.class_name = class_name
        self.class_definition = class_definition
        self.method_indexes = self.get_method_indexes()
        self.method_names = self.get_method_names()
        self.method_parameters = self.get_method_parameters()
        self.method_count = len(self.method_indexes)

    def get_method_indexes(self):
        """
        Used to return the lines numbers of methods in the class definition
        """
        method_indexes = []

        for i in range(len(self.class_definition)):
            method_regex = re.search(".{1}(def) ", self.class_definition[i])
            if method_regex:
                method_indexes.append(i)

        return method_indexes

    def get_method_names(self):
        """
        Extracts the method names from the line numbers
        """
        method_names = []

        for method_index in self.method_indexes:
            line = self.class_definition[method_index].lstrip()
            method_name = line.split()[1]
            method_name = method_name.split('(')[0]
            method_name += '()'
            method_names.append(method_name)

        return method_names

    def get_method_parameters(self):
        """
        Extracts the method attributes from the lines numbers
        """
        method_parameters = {}

        for i in range(len(self.method_indexes)):
            method_name = self.method_names[i]
            line = self.class_definition[self.method_indexes[i]].lstrip()
            attributes = line.split()[1]
            attributes = line.split('(')[1]
            attributes = attributes[:-2]
            attributes = attributes.split(',')

            method_parameters[method_name] = attributes

        return method_parameters

    def __str__(self):
        output_string = f"\t {self.get_method_count()} Method(s)\n"

        for method_name in self.method_names:
            output_string += '\t' + method_name + '\n'
            output_string += f"\t\t {len(self.method_parameters[method_name])} Parameter(s) \n"
            for attribute in self.method_parameters[method_name]:
                output_string += '\t\t' + attribute.lstrip() + '\n'

        return output_string

    def get_method_count(self):
        return self.method_count

    def get_class_name(self):
        return self.class_name
