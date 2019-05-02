'''
Question2 Description : 
	Write a program which can compute the factorial of a given numbers.
	The results should be printed in a comma-separated sequence on a single line.
	Suppose the following input is supplied to the program:
	8
	Then, the output should be:
	40320
'''
inp = int(input("Enter the number:"))
opt = 1
for i in range(1,inp+1):
	opt = opt*i

print(opt) 