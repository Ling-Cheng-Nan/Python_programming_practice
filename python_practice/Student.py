from Person import *

class Student(Person):
    
    def __init__(self, fname, lname, graduationyear):
        # print("Child constructor : Student.class")
        # self.fname = "first name : " + fname 
        # self.lname = "last name : " + lname 
        super().__init__(fname, lname)
        self.graduationyear = graduationyear

        def printname(self):
            print(self.fname, self.lname, graduationyear)

class NormalPerson(Person):

    #inherit from Person class
    def __init__(self, fname, lname):
        Person.__init__(self, fname, lname)

