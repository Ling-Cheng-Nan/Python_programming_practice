'''
    using the "from" keyword, do not use the module name when referring to elements in the module. Example: person1["age"], 
    not mymoduke.person1["age"]
'''
from Student import * # only part import from module, use "from [module_name] import [imported_parts]" 
import greet_module as greet
import platform
import datetime

# x = Student("Mike", "Olsen", 2019)
# x.printname()


# x = NormalPerson("Sam", "Ling")
# x.printname()

'''
    use function/code from other module
'''
# greet.greeting("Jonathan")
# a = greet.person1["age"]
# print(a)

''' test built-in module '''
# x = platform.system()
# print(x)

''' list all the function names (or variable names) in a module '''
# x = dir(greet)
# print(x)



x = datetime.datetime.now()

print(x.year)
print(x.strftime("%A"))