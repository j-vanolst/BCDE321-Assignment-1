class Animal:

    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hello, my name is {self.name}"


class Car:

    def __init__(self, brand, colour):
        self.brand = brand
        self.colour = colour

    def get_brand(self):
        return self.brand

    def get_colour(self):
        return self.colour
