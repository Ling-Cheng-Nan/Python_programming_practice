'''
Question17 Description:
Write a program that computes the net amount of a bank account based a transaction log from console input. 
The transaction log format is shown as following:
D 100
W 200

D means deposit while W means withdrawal.
Suppose the following input is supplied to the program:
D 300
D 300
W 200
D 100
Then, the output should be:
500

Hints:
In case of input data being supplied to the question, it should be assumed to be a console input.
'''
acc = {"D":0,"W":0}

while input("\n"):
	#print("there is standard input...")
	transaction = input("\n=> ")
	x = transaction.split(" ")
	print(x)
	'''
	try:
		if (x[0] == "D" or x[0] == "deposit" or x[0] == "Deposit"):
			acc["D"] += x[1]
		elif (x[0] == "W" or x[0] == "withdrawal" or x[0] == "Withdrawal"):
			acc["W"] += x[1]
	except:
		print("invalid transaction, please re-type one, or empty input will out of service...\n")
	'''

print(acc["D"]-acc["W"])
