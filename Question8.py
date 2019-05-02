'''
Question8 Description:
	Write a program that accepts a comma separated sequence of words as 
	input and prints the words in a comma-separated sequence after sorting them alphabetically.
	
	Suppose the following input is supplied to the program:
	without,hello,bag,world
	
	Then, the output should be:
	bag,hello,without,world
'''
input_str  = input()
w_list = list()
for word in input_str.split(','):
	w_list.append(word)

w_list.sort()
print(w_list)