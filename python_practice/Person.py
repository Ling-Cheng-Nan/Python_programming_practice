class Person:
  
    def __init__(self, fname, lname):
        print("Parent constructor : Person.class")
        self.fname = fname
        self.lname = lname

    def printname(self):
        print(self.fname, self.lname)


# class Student(Person):
#   def __init__(self, fname, lname):
#     Person.__init__(self, fname, lname)  

# x = Student("Mike", "Olsen")
# x.printname()