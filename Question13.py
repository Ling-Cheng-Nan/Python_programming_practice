'''
Question13 Description:
    
    Write a program that accepts a sentence and calculate the number of letters and digits.
    
    Suppose the following input is supplied to the program:
        hello world! 123
    
    Then, the output should be:
        LETTERS 10
        DIGITS 3

    Hints:
        In case of input data being supplied to the question, it should be assumed to be a console input.
'''
dic = { "LETTER":0,"DIGIT":0 }
in_seq = input("Enter a sequence of numbers and letters .....")

for letter in in_seq:
    try:
        if (letter.isdigit()):
            dic["DIGIT"]  += 1
        if (letter.isalpha()):
            dic["LETTER"] += 1
    except:
        print(letter+" is not either a alpha or digit!")

print(dic)
    

