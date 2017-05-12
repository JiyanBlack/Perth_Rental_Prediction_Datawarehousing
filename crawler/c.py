class Student:
    name = ''

    def __init__(self,name):
        self.name = name

    def print_name(self):
        print(self.name)


a = Student('abc')
a.print_name()
