#!/usr/bin/python3

class MyClass:

    def __init__(self):

        self.__a = 100

        self.b = 200

    def get_a(self):

        return self.__a

if __name__ == "__main__":

    mc = MyClass()

    print(mc.b)

    print(mc.get_a())

    print(mc.__a)
