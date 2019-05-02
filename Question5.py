'''
Question5 Description : 
	Define a class which has at least two methods:
	--getString   : to get a string from console input
	--printString : to print the string in upper case.
	Also please include simple test function to test the class methods.
'''

class SelfDefinedClass(object):
	
	def __init__(self):
		self.s = ""

	def getString(self):
		self.s = input("Enter string from console:")
	
	def printString(self):
		print(self.s.upper())


strObj = SelfDefinedClass()
strObj.getString()
strObj.printString()

