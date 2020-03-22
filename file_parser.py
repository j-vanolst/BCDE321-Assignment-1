import re

class ClassDefinition:


    def __init__(self, name, line_index, class_definition):
        self.name = name
        self.line_index = line_index
        self.class_definition = class_definition
        self.methods = []

    def get_name(self):
        print(self.name, self.line_index)
        return 0



f = open("test.py", 'r')
lines = f.read()
lines = lines.split('\n')

class_indexes = []


for i in range(len(lines)):
    if 'class' in lines[i]:
        class_indexes.append(i)

class_names = []
class_definitions = []


def get_class_name():

    for class_index in class_indexes:

        # Class Name
        words = lines[class_index].split(' ')

        x = re.findall("\w", words[1])

        class_name = ''
        class_name = class_name.join(x)

        class_names.append(class_name)

def get_class_definition():

    for i in range(len(class_indexes)):

        # Class Definition
        if i < len(class_indexes) - 1:
            end_index = class_indexes[i + 1]
        else:
            end_index = -1

        class_definition = list(lines[i:end_index])
        print(class_definition)

        class_definitions.append(class_definition)

get_class_name()
get_class_definition()

# for i in range(len(class_names)):
#     print(f"CLASS NAME: {class_names[i]}, CLASS DEFINITION: {class_definitions[i]}")